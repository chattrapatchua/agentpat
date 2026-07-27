# Work Agent MCP server

Project-local [Model Context Protocol](https://modelcontextprotocol.io) server so **Cursor Agent mode** can search/read/write `./knowledge` and list/run workflows from `.cursor/workflows/` using the same logic as the future web app.

Full design: [`agent/architecture.md`](../agent/architecture.md) (MCP server section). Implementation guide: [`packages/mcp-server/README.md`](../packages/mcp-server/README.md).

## Registration

| Command | Purpose |
| --- | --- |
| `./onboard-agent-dan` | First time — clone (optional), install, build, open Cursor |
| `./call-agent-dan` | Routine — install/build if needed, open Cursor |
| `./rename-agent-dan <slug>` | Rename agent; regenerates entrypoints |

Cursor starts MCP automatically via **`.cursor/mcp.json`** → `bash scripts/run-work-agent-mcp.sh`. Clone URL: `agent/default-repo.url`, `WORK_AGENT_REPO_URL`, or `--repo`.

## Environment

| Variable | Purpose |
| --- | --- |
| `WORK_AGENT_ROOT` | Absolute path to repo root (default: process cwd). Used to resolve `knowledge/`, `.cursor/workflows/`. |
| `WORK_AGENT_IDE_DIR` | IDE asset folder name (e.g. `.cursor`) from `agent/ide-target`; workflows/skills paths for `workflow_run`. |

Optional later: `WORK_AGENT_READ_ONLY=1` to disable `knowledge_write` from MCP.

## Tools (contract)

| Tool | Description |
| --- | --- |
| `knowledge_search` | Query `./knowledge` (text + metadata) |
| `knowledge_read` | Read a file under `./knowledge` |
| `knowledge_write` | Create/update a knowledge file (validated frontmatter) |
| `workflow_list` | List workflows in `.cursor/workflows/` |
| `workflow_run` | Execute workflow by `id` with `inputs` and optional `session_id` |

Tool names and JSON schemas are defined in `packages/mcp-server` and must stay aligned with **agent-core** (web API uses the same handlers).

## Workflows and major-task completion

For deliverable workflows (especially **`learn-knowledge`**), prefer **`workflow_run`** over informal chat so every step loads into the agent context (including **task-completion-gate**, **samectx**, **retrospective**).

Example:

```json
{ "id": "learn-knowledge", "inputs": { "topic": "your topic" } }
```

Execute steps **in order** across chat turns:

1. Research and user confirm → store to `./knowledge/` (research **yes** ≠ task done).
2. **task-completion-gate** — **AskQuestion** (**Mark task done** / Not yet / Pause)
3. On **Mark task done** → **samectx** → **retrospective** (`./adr/`, `./knowledge/`).

For **ad-hoc major tasks** (no workflow id), follow `.cursor/rules/99-task-completion-gate.mdc` after the deliverable is finished.

After changing `packages/agent-core`, run `npm run build` from repo root so MCP serves updated `workflow_run` summaries.

## Security

- Stdio transport only for desktop Cursor (local OS user trust boundary).
- No secrets in tool responses; paths jailed to `knowledge/` and `.cursor/workflows/`.
- Do not expose this MCP process to the public internet; the web app uses HTTP API + agent-core instead.
