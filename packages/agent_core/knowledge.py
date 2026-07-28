"""Knowledge service: search / read / write over ./knowledge with a path jail.

Shared by the MCP server and the web agent loop. Reads and writes are confined to
the knowledge directory; escaping paths raise instead of touching the filesystem.
"""
from __future__ import annotations

import yaml

from . import config


class KnowledgeError(Exception):
    """Not found, path escape, validation failure, or read-only violation."""


def _safe_path(rel: str) -> "config.Path":
    from pathlib import Path

    if not rel:
        raise KnowledgeError("path is required")
    base = config.KNOWLEDGE_DIR.resolve()
    candidate = (base / rel).resolve()
    if candidate != base and base not in candidate.parents:
        raise KnowledgeError(f"path escapes knowledge/: {rel}")
    return candidate


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split leading `--- ... ---` YAML frontmatter from the markdown body."""
    if not text.startswith("---"):
        return {}, text
    lines = text.splitlines()
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, text
    try:
        meta = yaml.safe_load("\n".join(lines[1:end])) or {}
        if not isinstance(meta, dict):
            meta = {}
    except yaml.YAMLError:
        meta = {}
    return meta, "\n".join(lines[end + 1:]).lstrip("\n")


def search(query: str, limit: int = 10) -> list[dict]:
    """Case-insensitive filename + body substring search. Ranked; empty list if none."""
    if not query or not query.strip():
        raise KnowledgeError("query is required")
    q = query.lower()
    base = config.KNOWLEDGE_DIR
    if not base.exists():
        return []

    results: list[dict] = []
    for path in sorted(base.rglob("*.md")):
        rel = path.relative_to(base).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        meta, _ = parse_frontmatter(text)
        title = str(meta.get("title") or path.stem)
        name_hit = q in rel.lower() or q in title.lower()
        low = text.lower()
        body_count = low.count(q)
        if not name_hit and body_count == 0:
            continue
        idx = low.find(q)
        snippet = ""
        if idx != -1:
            start, stop = max(0, idx - 60), min(len(text), idx + len(q) + 60)
            snippet = text[start:stop].replace("\n", " ").strip()
        results.append(
            {
                "path": rel,
                "title": title,
                "score": (2 if name_hit else 0) + body_count,
                "snippet": snippet,
            }
        )
    results.sort(key=lambda r: r["score"], reverse=True)
    return results[:limit]


def read(path: str) -> dict:
    """Read one knowledge file. Raises KnowledgeError if missing or outside the jail."""
    p = _safe_path(path)
    if not p.exists() or not p.is_file():
        raise KnowledgeError(f"not found: {path}")
    text = p.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)
    return {"path": path, "frontmatter": meta, "content": text, "body": body}


def write(path: str, content: str, frontmatter: dict | None = None) -> dict:
    """Create/update a .md note under knowledge/. Returns a dedupe hint by title."""
    if config.READ_ONLY:
        raise KnowledgeError("read-only mode (WORK_AGENT_READ_ONLY=1)")
    if not path.endswith(".md"):
        raise KnowledgeError("knowledge files must end with .md")

    p = _safe_path(path)
    existed = p.exists()
    body = content or ""

    if frontmatter and not body.startswith("---"):
        fm = yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True).strip()
        body = f"---\n{fm}\n---\n\n{body}"

    title = (frontmatter or parse_frontmatter(body)[0]).get("title")
    dupes: list[str] = []
    if title:
        try:
            dupes = [r["path"] for r in search(str(title)) if r["path"] != path][:5]
        except KnowledgeError:
            dupes = []

    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return {
        "path": path,
        "bytes": len(body.encode("utf-8")),
        "created": not existed,
        "duplicate_titles": dupes,
    }
