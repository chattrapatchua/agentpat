# MVP — try Work Agent in Cursor

Goal: use **Agent mode** in this repo with **work-agent** MCP tools over `./knowledge` and `.cursor/workflows`, without the web UI.

## In scope

| Item | MVP behavior |
| --- | --- |
| MCP server | stdio, name **work-agent**, five tools |
| `knowledge_search` | Filename + body substring search under `./knowledge` |
| `knowledge_read` | Read one file (path jailed) |
| `knowledge_write` | Create/update markdown under `./knowledge` |
| `workflow_list` | List workflows from `.cursor/workflows/**/*.yaml` |
| `workflow_run` | Load workflow; for `skill` steps, embed `.cursor/skills/{ref}/SKILL.md` in the tool result so the Cursor model executes the flow |
| Sample data | One knowledge note + one example workflow |
| Docs | This file + `.cursor/MCP.md` |

## Out of scope (later)

- Web chat, embeddings/RAG, full automated workflow engine with model calls inside MCP
- `prompt` / `tool` workflow steps executed server-side (returned as instructions only)
- Auth, session DB, CI eval harness

## Prerequisites

- Node.js 20+
- Cursor with MCP enabled for this workspace

## Try it

**First machine / fresh clone:**

```bash
./onboard-agent-dan
# clones https://github.com/ethanhuangcst/agent-dan.git when run outside the repo
# asks which IDE you use (Claude / Codex / Cursor / Other) and deploys rules, skills, workflows to .{ide}/
```

Non-interactive: `./onboard-agent-dan --ide cursor --non-interactive`

**Already have the repo:**

```bash
./call-agent-dan
# or: make call-agent-dan
# or: npm run call-agent-dan
```

**Rename the agent** (e.g. to `alex`):

```bash
./rename-agent-dan alex
# then use: ./call-agent-alex
```

This runs **install** and **build** only when needed, then opens **Cursor**. MCP **work-agent** starts from `.cursor/mcp.json` (`scripts/run-work-agent-mcp.sh`).

Use `call-agent-dan --fresh` to force reinstall and rebuild.

In Cursor:

1. **Settings → MCP** — confirm **work-agent** is enabled (once per machine).
2. **Agent mode** — example prompts:

   - “Use `knowledge_search` for discovery and summarize what you find.”
   - “`knowledge_read` the getting-started note and give me three bullets.”
   - “`workflow_list` then `workflow_run` the hello workflow with theme ‘AI coaching’.”
   - **Learn Knowledge:** Prefer MCP **`workflow_run`** with `{ "id": "learn-knowledge", "inputs": { "topic": "…" } }` so completion-gate steps load. Natural language (“learn-knowledge on …”) is OK if the agent follows the full YAML through samectx and retrospective.
   - After any **major task** (feature slice, KB write, multi-step scope), the agent must use **AskQuestion** (**Mark task done** / Not yet / Pause) then run samectx + retrospective per **`99-task-completion-gate.mdc`**.

5. **Optional skill** — `/research-ops` or `/knowledge-ops`; workflows via `workflow_run`.

## Success criteria

- MCP **work-agent** shows connected in Cursor.
- Agent turn log shows tool calls to `knowledge_*` or `workflow_*` with sensible JSON results.
- A new file appears under `./knowledge/` after `knowledge_write` (or you approve the write).

## If MCP fails to start

- Run `node packages/mcp-server/dist/index.js` from repo root — should hang on stdio (no error).
- Check Node path in Cursor MCP settings matches your shell (`which node`).
- See `.cursor/MCP.md`.

## After MVP

Phase 2 in `agent/architecture.md`: web UI sharing `packages/agent-core`. Phase 3: FTS/embeddings for search.
