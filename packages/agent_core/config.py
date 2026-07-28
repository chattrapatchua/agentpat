"""Central configuration and path resolution.

Every downstream module (knowledge, workflows, MCP server, web app) resolves paths
through here, so the repo root is computed exactly one way.
"""
from __future__ import annotations

import os
from pathlib import Path


def _default_root() -> Path:
    # packages/agent_core/config.py -> repo root is two parents above the package dir.
    return Path(__file__).resolve().parents[2]


ROOT = Path(os.environ.get("WORK_AGENT_ROOT", str(_default_root()))).resolve()

# Load a local .env if present (web loop reads model keys from it). Never required.
try:  # pragma: no cover - convenience only
    from dotenv import load_dotenv

    load_dotenv(ROOT / ".env")
except Exception:
    pass

KNOWLEDGE_DIR = ROOT / "knowledge"
WORKFLOWS_DIR = ROOT / ".cursor" / "workflows"
SKILLS_DIR = ROOT / ".cursor" / "skills"

# Optional write guard for shared machines (see architecture.md, Security).
READ_ONLY = os.environ.get("WORK_AGENT_READ_ONLY") == "1"

# Model config — used only by the WEB agent loop. The MCP path uses Cursor's own model.
ANTHROPIC_MODEL = os.environ.get("WORK_AGENT_MODEL", "claude-sonnet-5")
OPENAI_MODEL = os.environ.get("WORK_AGENT_OPENAI_MODEL", "gpt-4o")
MAX_STEPS = int(os.environ.get("WORK_AGENT_MAX_STEPS", "8"))


def agent_name() -> str:
    """The agent's slug, read from agent/agent-name (falls back to 'work-agent')."""
    try:
        return (ROOT / "agent" / "agent-name").read_text(encoding="utf-8").strip() or "work-agent"
    except OSError:
        return "work-agent"
