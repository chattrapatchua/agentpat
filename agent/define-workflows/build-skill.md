# build-skill workflow

Interactive workflow to author a new Agent Skill from user context: five **AskQuestion** gathers → composed brief → **skill-creator** → `agent/define-skills/<slug>/` → deploy to `$IDE_DIR/skills/`.

## Run

```json
{ "id": "build-skill", "inputs": { "skill_hint": "optional-kebab-name" } }
```

Prefer MCP **`workflow_run`** so all steps load in order.

## Steps

| # | id | Type | Purpose |
| --- | --- | --- | --- |
| 1 | gather-context | prompt | Q1 — situation (first-person → brief) |
| 2 | gather-role | prompt | Q2 — role / expertise |
| 3 | gather-knowledge | prompt | Q3 — KB / topics |
| 4 | gather-behavior | prompt | Q4 — expected behavior |
| 5 | gather-rules | prompt | Q5 — output rules |
| 6 | compose-skill-brief | prompt | Situation / Role / Knowledge / Task / Rule block + approve |
| 7 | name-skill | prompt | kebab-case slug |
| 8 | prepare-skill-creator | prompt | Handoff to skill-creator |
| 9 | create-skill | skill | `skill-creator` |
| 10 | deploy-skill | prompt | `deploy-ide-assets.sh` |
| 11–13 | task-completion-gate → samectx → retrospective | | Major-task close |

## Prompt template

Composed block shape (step 6):

```markdown
# Situation   ← Q1
# Role        ← Q2
# Knowledge   ← Q3
# Task        ← default KB/learn-knowledge + Q4
# Rule        ← Q5
```

Production: [`.cursor/workflows/discovery/build-skill.yaml`](../../.cursor/workflows/discovery/build-skill.yaml)

Prompts: [`.cursor/workflows/prompts/build-skill/`](../../.cursor/workflows/prompts/build-skill/)
