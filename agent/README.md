# Work Agent — design and authoring

This folder holds **human-facing agent design** and **draft** definitions. Runtime assets live elsewhere (see table below).

| Path | Purpose |
| --- | --- |
| [`context.md`](context.md) | Situation and task (why this agent exists) |
| [`architecture.md`](architecture.md) | Technical architecture (clients, MCP, knowledge, workflows) |
| [`mvp-cursor.md`](mvp-cursor.md) | **MVP: try the agent in Cursor** (install, prompts, success criteria) |
| [`define-rules/`](define-rules/) | Draft Cursor rules → promote to `.cursor/rules/` |
| [`define-skills/`](define-skills/) | Draft skills → promote to `.cursor/skills/` |
| [`define-workflows/`](define-workflows/) | Draft workflows → promote to `.cursor/workflows/` |

## Production vs draft

| Concern | Draft | Production |
| --- | --- | --- |
| Rules | `agent/define-rules/` | `.cursor/rules/` |
| Skills | `agent/define-skills/` | `.cursor/skills/` |
| Workflows | `agent/define-workflows/` | `.cursor/workflows/` |
| Knowledge | (author in repo) | `./knowledge/` |
| MCP (Cursor tools) | — | `packages/mcp-server/` + [`.cursor/mcp.json`](../.cursor/mcp.json) |

Entrypoint for Cursor agents: [`AGENTS.md`](../AGENTS.md) and [`.cursor/MCP.md`](../.cursor/MCP.md).
