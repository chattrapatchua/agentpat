#!/usr/bin/env bash
# After agent stop: nudge task-completion AskQuestion when edits suggest a major task and gate not done.
set -euo pipefail
input=$(cat)
status=$(echo "$input" | jq -r '.status // empty')
loop_count=$(echo "$input" | jq -r '.loop_count // 0')
conv_id=$(echo "$input" | jq -r '.conversation_id // "default"')
root=$(echo "$input" | jq -r '.workspace_roots[0] // empty')
[[ -z "$root" ]] && root="$(pwd)"

if [[ "$status" != "completed" ]]; then
  echo '{}'
  exit 0
fi

if [[ ! -f "$root/package.json" ]] || ! grep -q '"name"[[:space:]]*:[[:space:]]*"work-agent"' "$root/package.json" 2>/dev/null; then
  echo '{}'
  exit 0
fi

state_file="$root/.cursor/hooks/.gate-state.json"
edits=0
gate_done=false
if [[ -f "$state_file" ]]; then
  read -r edits gate_done < <(python3 - "$state_file" "$conv_id" <<'PY'
import json, sys
path, conv = sys.argv[1], sys.argv[2]
with open(path) as f:
    data = json.load(f)
entry = data.get(conv, {})
print(int(entry.get("edits", 0)), "true" if entry.get("gate_done") else "false")
PY
)
fi

transcript=$(echo "$input" | jq -r '.transcript_path // empty')
if [[ -n "$transcript" && -f "$transcript" ]]; then
  if grep -qE 'mark-task-done|"Mark task done"|samectx sync|Retrospective Summary' "$transcript" 2>/dev/null; then
    gate_done=true
    python3 - "$state_file" "$conv_id" <<'PY' 2>/dev/null || true
import json, sys, os
path, conv = sys.argv[1], sys.argv[2]
if not os.path.isfile(path):
    sys.exit(0)
with open(path) as f:
    data = json.load(f)
if conv in data:
    data[conv]["gate_done"] = True
    data[conv]["edits"] = 0
with open(path, "w") as f:
    json.dump(data, f)
PY
  fi
fi

# Skip if gate already satisfied or not enough substantive edits
if [[ "$gate_done" == true ]] || [[ "$edits" -lt 2 ]]; then
  echo '{}'
  exit 0
fi

if [[ "$loop_count" -ge 3 ]]; then
  echo '{}'
  exit 0
fi

jq -n --arg msg "Continuous-learning gate: This session changed multiple files. If the major task scope is complete, you must invoke AskQuestion per .cursor/rules/99-task-completion-gate.mdc (Mark task done / Not yet / Pause) before ending. If work continues or this was not a major task, say so in one sentence." \
  '{followup_message: $msg}'
exit 0
