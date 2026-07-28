# work-agent MCP server

stdio MCP server that exposes the shared `agent_core` tools to Cursor Agent mode.

| Tool | Delegates to |
| --- | --- |
| `knowledge_search` | `agent_core.knowledge.search` |
| `knowledge_read` | `agent_core.knowledge.read` |
| `knowledge_write` | `agent_core.knowledge.write` |
| `workflow_list` | `agent_core.workflow.list_workflows` |
| `workflow_run` | `agent_core.workflow.run` |

## Run

Cursor starts it automatically via [`.cursor/mcp.json`](../../.cursor/mcp.json) →
`bash scripts/run-work-agent-mcp.sh`. To smoke-test by hand from the repo root:

```bash
.venv/Scripts/python -m mcp_server.server   # Windows (Git Bash)
.venv/bin/python -m mcp_server.server       # macOS / Linux
```

It should hang silently on stdio (no output, no error) — that means it's waiting for
an MCP client. Ctrl-C to exit.

## Notes

- Errors are returned as `{"error","message"}` JSON, never raised to the client.
- No model calls happen here; Cursor supplies the model. The web app (`apps/web`) has
  its own agent loop over the same tools.
- Set `WORK_AGENT_READ_ONLY=1` to block `knowledge_write` on shared machines.
