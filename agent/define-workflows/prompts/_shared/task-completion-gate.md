# Shared — Task completion gate (continuous learning)

Use at the end of **major-task** workflows after deliverables are written. Complements `.cursor/rules/continuous-learning.mdc` and **`99-task-completion-gate.mdc`**.

## Two different confirmations

If this workflow already asked the user to confirm research, content, or storage, that **yes** is **not** task completion. Do not run samectx or retrospective until the user confirms in **this** step.

## Structured prompt (required — not plain chat yes/no)

Do **not** ask only in chat: *Can I mark this as done?* Bare **yes** / **looks good** after research or storage must not trigger samectx or retrospective.

Use the **AskQuestion** tool (in-chat choice panel). One question:

**Prompt:** `Close this major task? (Separate from research or storage confirmation.)`

| Option `id` | Label |
| --- | --- |
| `mark-task-done` | **Mark task done** — run samectx sync and retrospective |
| `not-yet` | **Not yet** — more work on this task |
| `pause-no-sync` | **Pause here** — stop without samectx or retrospective |

**Only** `mark-task-done` authorizes samectx and retrospective.

If AskQuestion is unavailable, require the exact phrase **Mark task done** in chat (not bare **yes**).

## After `mark-task-done`

1. **samectx** — `samectx sync` with `--tasks`, `--keypoints`, `--decisions` (semicolon-separated; no secrets).
2. **retrospective** — ADRs → `./adr/`; knowledge → `./knowledge/`; present Retrospective Summary.

Do not commit unless the user requests a commit.

## Used by

- `learn-knowledge` → `prompts/learn-knowledge/05-task-completion-gate.md`

Copy or reference this file when adding completion gates to other workflows (see `agent/define-workflows/workflow.md`).
