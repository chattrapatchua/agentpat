#!/usr/bin/env bash
# After knowledge_write: remind agent that store yes is not task-done (continuous-learning).
set -euo pipefail
input=$(cat)
tool=$(echo "$input" | jq -r '.tool_name // .tool // empty')
if [[ "$tool" != *"knowledge_write"* ]]; then
  echo '{}'
  exit 0
fi
jq -n '{additional_context: "Research/store confirmation is complete only for knowledge_write. Continue the workflow: task-completion-gate (AskQuestion: Mark task done / Not yet / Pause) → samectx → retrospective per .cursor/rules/99-task-completion-gate.mdc. Do not end the session after storage."}'
exit 0
