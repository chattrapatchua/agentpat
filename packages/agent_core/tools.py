"""Tool registry shared by the MCP server and the web agent loop.

Each tool has a name, a description that states its failure modes (so the model picks
correctly), a JSON-schema input, and a handler(args) -> dict. Because both transports
call through here, Cursor and the web app expose identical tool contracts.
"""
from __future__ import annotations

from . import knowledge, workflow


def _knowledge_search(args: dict) -> dict:
    res = knowledge.search(args["query"], int(args.get("limit", 10)))
    return {"results": res, "count": len(res)}


def _knowledge_read(args: dict) -> dict:
    return knowledge.read(args["path"])


def _knowledge_write(args: dict) -> dict:
    return knowledge.write(args["path"], args.get("content", ""), args.get("frontmatter"))


def _workflow_list(args: dict) -> dict:
    items = workflow.list_workflows()
    return {"workflows": items, "count": len(items)}


def _workflow_run(args: dict) -> dict:
    return workflow.run(args["id"], args.get("inputs") or {}, args.get("session_id"))


TOOLS: list[dict] = [
    {
        "name": "knowledge_search",
        "description": (
            "Search ./knowledge by filename and body substring (case-insensitive). "
            "Returns ranked {path,title,snippet,score}. Empty list if nothing matches; "
            "raises on an empty query. Use before answering factual questions."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Substring to search for."},
                "limit": {"type": "integer", "description": "Max results (default 10)."},
            },
            "required": ["query"],
        },
        "handler": _knowledge_search,
    },
    {
        "name": "knowledge_read",
        "description": (
            "Read one knowledge file by path relative to knowledge/ (path-jailed). "
            "Returns frontmatter + full content. Errors if the file is missing or escapes the jail."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "e.g. methods/getting-started.md"},
            },
            "required": ["path"],
        },
        "handler": _knowledge_read,
    },
    {
        "name": "knowledge_write",
        "description": (
            "Create or update a .md note under knowledge/. Optionally supply frontmatter "
            "(id/title/tags/...) which is prepended when the content has none. Returns a dedupe "
            "hint listing existing notes with the same title. Rejected in read-only mode or on path escape."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Target path under knowledge/, must end .md"},
                "content": {"type": "string", "description": "Markdown body (may already include frontmatter)."},
                "frontmatter": {"type": "object", "description": "Optional YAML frontmatter fields."},
            },
            "required": ["path", "content"],
        },
        "handler": _knowledge_write,
    },
    {
        "name": "workflow_list",
        "description": "List available workflows from .cursor/workflows/**/*.yaml with their inputs.",
        "input_schema": {"type": "object", "properties": {}},
        "handler": _workflow_list,
    },
    {
        "name": "workflow_run",
        "description": (
            "Run a workflow by id. skill steps embed the referenced SKILL.md; prompt/tool steps "
            "return instructions for you to execute. Errors on unknown id or missing required inputs."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "Workflow id, e.g. hello or learn-knowledge."},
                "inputs": {"type": "object", "description": "Workflow inputs by name."},
                "session_id": {"type": "string", "description": "Optional correlation id."},
            },
            "required": ["id"],
        },
        "handler": _workflow_run,
    },
]

TOOLS_BY_NAME = {t["name"]: t for t in TOOLS}


def call(name: str, args: dict | None) -> dict:
    """Dispatch a tool by name. Raises KeyError for an unknown tool."""
    tool = TOOLS_BY_NAME.get(name)
    if not tool:
        raise KeyError(f"unknown tool: {name}")
    return tool["handler"](args or {})


def anthropic_schemas() -> list[dict]:
    return [
        {"name": t["name"], "description": t["description"], "input_schema": t["input_schema"]}
        for t in TOOLS
    ]


def openai_schemas() -> list[dict]:
    return [
        {
            "type": "function",
            "function": {
                "name": t["name"],
                "description": t["description"],
                "parameters": t["input_schema"],
            },
        }
        for t in TOOLS
    ]
