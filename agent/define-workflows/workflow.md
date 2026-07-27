# Workflow authoring (draft → production)

Design workflows in this folder, then promote to [`.cursor/workflows/`](../../.cursor/workflows/) as validated YAML. Runtime: MCP `workflow_list` / `workflow_run` and Cursor Agent (model executes steps; skills and prompts are loaded into context).

See also: [`agent/architecture.md`](../architecture.md) (workflow schema), [`.cursor/workflows/README.md`](../../.cursor/workflows/README.md).

## Draft vs production

| Phase | Location |
| --- | --- |
| Authoring notes | `agent/define-workflows/*.md` |
| Executable definition | `.cursor/workflows/**/*.yaml` |
| Prompt templates | `.cursor/workflows/prompts/<workflow-id>/` |

Keep draft markdown in sync when you change production YAML.

## YAML shape

```yaml
id: kebab-case-id          # workflow_run id
version: 1
title: Human title
description: When to use this workflow
interactive: true          # set when steps span multiple chat turns
inputs:
  - name: topic
    type: string
    required: false
steps:
  - id: step-id
    type: prompt | skill | tool
    template: prompts/...   # when type: prompt
    ref: skill-folder-name    # when type: skill → .cursor/skills/{ref}/SKILL.md
```

## Step types (MVP)

| Type | Purpose | Agent behavior |
| --- | --- | --- |
| `prompt` | Scripted turn: questions, gates, format | Follow template across one or more chat turns until satisfied |
| `skill` | Reusable procedure | Read embedded `SKILL.md`; apply guardrails and tools as described |
| `tool` | Side effect via MCP | Invoke registered tool with templated args (when implemented server-side) |

Steps run in **list order**. For `interactive: true`, the agent may pause between steps until user input is required.

## How to structure steps

1. **Inputs** — Capture scope early (`topic`, `theme`, flags). Optional inputs should say in the first prompt what to ask if missing.
2. **Skills for heavy procedure** — Research, KB writes, sync, retrospective: use `type: skill` with `ref` matching `.cursor/skills/<ref>/`.
3. **Prompts for human gates** — Confirmations, revision loops, exact questions: use `type: prompt` with templates under `prompts/<workflow>/`.
4. **Separate “content yes” from “task done”** — If the workflow asks “confirm research before store”, that **yes** must not skip the completion gate. After deliverables are written, add an explicit **task completion** prompt (see learn-knowledge step 5).
5. **Completion gate (major tasks)** — Workflows that finish a coherent deliverable (research + KB, feature slice, multi-step integration) should end with the **continuous-learning** pattern:
   - Prompt: use [`../../.cursor/workflows/prompts/_shared/task-completion-gate.md`](../../.cursor/workflows/prompts/_shared/task-completion-gate.md) (or a workflow-specific wrapper that links to it).
   - Skill: `samectx` — sync session notes to `samectx-notes/`.
   - Skill: `retrospective` — ADRs → `./adr/`, knowledge → `./knowledge/` (often `ops/` for process lessons).
   - Rule reference: `.cursor/rules/continuous-learning.mdc` and **`99-task-completion-gate.mdc`**.

**Reusable YAML tail** (append to deliverable workflows):

```yaml
  - id: task-completion-gate
    type: prompt
    template: prompts/_shared/task-completion-gate.md
  - id: samectx-sync
    type: skill
    ref: samectx
  - id: retrospective
    type: skill
    ref: retrospective
```

6. **Domain vs ops knowledge** — `./knowledge/` holds MCP-visible notes (`methods/`, `insights/`, `ops/`, etc.). Retrospective ADRs go to `./adr/`; retrospective lessons go under `./knowledge/` (typically `ops/`). Ad-hoc major tasks without YAML still use the rules when the deliverable is complete.

## Promotion checklist

1. Write or update draft doc in `agent/define-workflows/<name>.md`.
2. Add or update `.cursor/workflows/<category>/<id>.yaml`.
3. Add prompt files under `.cursor/workflows/prompts/<id>/`.
4. Ensure referenced skills exist under `.cursor/skills/<ref>/SKILL.md`.
5. Test: `workflow_list`, then `workflow_run` with `{ "id": "...", "inputs": { ... } }`.
6. Update `agent/define-workflows/README.md` or this file if conventions change.

## Example: learn-knowledge

See [`learn-knowledge.md`](learn-knowledge.md) — clarify → research (`research-ops`) → confirm loop → store (`knowledge-ops`) → KB write → task completion gate → `samectx` → `retrospective`.
