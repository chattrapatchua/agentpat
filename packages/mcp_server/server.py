"""work-agent MCP server (stdio) — exposes the shared tool registry to Cursor.

Thin adapter: every tool delegates to agent_core so the web app and Cursor share one
implementation. Errors are returned as structured {error, message} JSON, never raised
to the client and never as stack traces.
"""
from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

from agent_core import tools

mcp = FastMCP("work-agent")


def _run(name: str, args: dict) -> str:
    try:
        return json.dumps(tools.call(name, args), default=str, indent=2)
    except Exception as exc:
        return json.dumps({"error": type(exc).__name__, "message": str(exc)})


@mcp.tool()
def knowledge_search(query: str, limit: int = 10) -> str:
    """Search ./knowledge by filename + body substring. Ranked matches; empty if none."""
    return _run("knowledge_search", {"query": query, "limit": limit})


@mcp.tool()
def knowledge_read(path: str) -> str:
    """Read one knowledge file by path (relative to knowledge/, path-jailed). Errors if missing."""
    return _run("knowledge_read", {"path": path})


@mcp.tool()
def knowledge_write(path: str, content: str, frontmatter: dict | None = None) -> str:
    """Create/update a .md file under knowledge/. Read-only mode and path escapes are rejected."""
    return _run("knowledge_write", {"path": path, "content": content, "frontmatter": frontmatter})


@mcp.tool()
def workflow_list() -> str:
    """List workflows from .cursor/workflows/**/*.yaml."""
    return _run("workflow_list", {})


@mcp.tool()
def workflow_run(id: str, inputs: dict | None = None, session_id: str | None = None) -> str:
    """Run a workflow by id. skill steps embed SKILL.md; prompt/tool steps return instructions."""
    return _run("workflow_run", {"id": id, "inputs": inputs or {}, "session_id": session_id})


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
