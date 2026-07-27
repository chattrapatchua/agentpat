---
id: continuous-learning-gate
title: Continuous-learning gate — workflow vs rule-only
tags: continuous-learning, workflows, cursor, ops
created: "2026-07-27"
updated: "2026-07-27"
source: retrospective
related:
  - adr/ADR-001-learn-knowledge-completion-gate.md
  - adr/ADR-002-structured-task-done-askquestion.md
---

# Continuous-learning gate — workflow vs rule-only

## Summary

Relying on `.cursor/rules/continuous-learning.mdc` alone did not produce samectx sync or retrospective after a completed **learn-knowledge** run. The agent stored `./knowledge/` and stopped without a separate task-done gate. User **yes** to research confirmation was scoped to `knowledge_write`, not task completion.

## Follow-up (2026-07-27)

Task-done confirmation must use **AskQuestion** with explicit options (**Mark task done** / Not yet / Pause), not plain chat *Can I mark this as done?* — see `.cursor/workflows/prompts/_shared/task-completion-gate.md` and updated **`99-task-completion-gate.mdc`**. The Cursor “How did the agent do?” bar is not agent-controllable.

## Follow-up (2026-07-27, hooks)

**Trigger stack:** (1) always-on rules → agent must **AskQuestion**; (2) `workflow_run` YAML steps; (3) `.cursor/hooks.json` — `afterFileEdit` counts edits, `stop` may inject follow-up, `postToolUse` on `knowledge_write` reminds store ≠ task done. Hooks require **Cursor Hooks** enabled and project `.cursor/hooks.json` present (deploy copies with IDE assets).

## Evidence

- Rule requires: ask before closing → on confirm → samectx → retrospective.
- **learn-knowledge** ended at `04-store.md` with no completion step.
- `workflow_run` embeds skills/prompts but does not execute samectx or retrospective server-side.
- Global DoD retrospective gate was also skipped in the same session.

## Lesson / guidance

1. For major interactive workflows, add explicit YAML steps: **task-completion-gate** prompt → **samectx** skill → **retrospective** skill (see `agent/define-workflows/workflow.md`).
2. Prompts must state that **research/store yes ≠ task-done yes**.
3. Verify project `.cursor/rules/` are active in Cursor for the workspace; treat `AGENTS.md` as backup, not the only hook.
4. Retrospective outputs: ADRs → `./adr/`; ops/process lessons → `./knowledge/ops/` (domain/method notes may use `methods/`, `insights/`, etc.).

## Links

- [ADR-001](../../adr/ADR-001-learn-knowledge-completion-gate.md)
- `.cursor/workflows/prompts/learn-knowledge/05-task-completion-gate.md`
