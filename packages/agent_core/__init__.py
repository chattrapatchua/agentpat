"""Shared agent core for the Work Agent.

One implementation of knowledge, workflows, and the tool registry — reused by the
MCP server (Cursor) and the web chat API. Only the transport differs.
"""

__all__ = ["config", "knowledge", "workflow", "tools", "loop"]
