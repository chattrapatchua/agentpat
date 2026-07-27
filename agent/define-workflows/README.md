# Draft workflows

Markdown (and notes) for designing workflows before promotion.

**Production (runtime):** [`.cursor/workflows/`](../../.cursor/workflows/)

**How to author:** [`workflow.md`](workflow.md) — step types, structure, completion gate, promotion checklist.

When a workflow is ready:

1. Convert the draft to validated YAML (see `agent/architecture.md` workflow schema and `workflow.md`).
2. Place the file under `.cursor/workflows/` (e.g. `discovery/market-scan.yaml`).
3. Add prompt templates under `.cursor/workflows/prompts/<workflow-id>/` when using `type: prompt`.
4. Test via MCP `workflow_list` and `workflow_run` after the MCP server is built.

**Workflows in production:** `learn-knowledge`, `build-skill` (see [`build-skill.md`](build-skill.md)), `hello`.
