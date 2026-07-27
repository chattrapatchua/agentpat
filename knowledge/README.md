# Knowledge base

Git-tracked domain and method knowledge for the Work Agent. Consumed by:

- MCP tools `knowledge_search`, `knowledge_read`, `knowledge_write` ([`packages/mcp-server`](../packages/mcp-server/README.md))
- Web chat agent core (same handlers as MCP)
- Cursor Agent (via MCP or direct file read)

Conventions and layout: [`agent/architecture.md`](../agent/architecture.md) (Knowledge subsystem).

Use YAML frontmatter: `id`, `title`, `tags`, `created`, `updated`, `source`, `related[]`.

## Layout

| Path | Purpose |
| --- | --- |
| `methods/` | Frameworks, playbooks, procedural method notes |
| `insights/` | Synthesized research findings (dated) |
| `ops/` | Process and agent-ops lessons (often from retrospective) |
| `references/` | External source summaries (optional) |

Architecture decisions live in [`../adr/`](../adr/) (not under `knowledge/`).

## Index (ops)

| Doc | Topic | Updated |
| --- | --- | --- |
| [ops/continuous-learning-gate.md](ops/continuous-learning-gate.md) | When samectx/retrospective run; workflow vs rule | 2026-07-27 |
