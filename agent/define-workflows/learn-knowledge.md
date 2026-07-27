# Learn Knowledge (draft)

Production workflow: [`.cursor/workflows/discovery/learn-knowledge.yaml`](../../.cursor/workflows/discovery/learn-knowledge.yaml)  
Workflow id: **`learn-knowledge`** (replaces `learn-new-knowledge`).

Authoring conventions: [`workflow.md`](workflow.md).

## Purpose

Interactive learning: research with user in the loop, confirm before write, persist to `./knowledge/`, then close the major task with **continuous-learning** (samectx + retrospective).

## Steps

| Step | id | Type | Behavior |
| --- | --- | --- | --- |
| 1 | clarify-topic | prompt | Ask what to learn if `topic` input empty; use chat context |
| 2 | research | skill `research-ops` | Evidence from web/search + user messages |
| 3 | summarize-and-confirm | prompt | Summary in research-ops format; ask yes or feedback |
| 4 | revision-loop | prompt | Re-research on feedback until user says yes to **store** |
| 5 | store | skill `knowledge-ops` | Dedupe, consolidate |
| 6 | store-instructions | prompt | MCP `knowledge_write` to `./knowledge/` |
| 7 | task-completion-gate | prompt | **AskQuestion** — **Mark task done** / Not yet / Pause; research **yes** ≠ task done |
| 8 | samectx-sync | skill `samectx` | After user confirms done: `samectx sync` → `samectx-notes/` |
| 9 | retrospective | skill `retrospective` | `./adr/` + `./knowledge/` + Retrospective Summary |

Rule reference: [`.cursor/rules/continuous-learning.mdc`](../../.cursor/rules/continuous-learning.mdc).

## Natural language

- “Run **learn-knowledge** workflow.”
- “Start learn-knowledge on social media marketing.”

## MCP

`workflow_run` with `{ "id": "learn-knowledge", "inputs": { "topic": "optional" } }` — follow loaded steps across **multiple chat turns** through storage and, after explicit task-done confirmation, samectx and retrospective.
