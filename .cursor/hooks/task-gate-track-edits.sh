#!/usr/bin/env bash
# Bump per-conversation edit counter (major-task heuristic for stop hook).
set -euo pipefail
input=$(cat)
conv_id=$(echo "$input" | jq -r '.conversation_id // "default"')
root=$(echo "$input" | jq -r '.workspace_roots[0] // empty')
[[ -z "$root" ]] && root="$(pwd)"
state_dir="$root/.cursor/hooks"
state_file="$state_dir/.gate-state.json"
mkdir -p "$state_dir"
python3 - "$state_file" "$conv_id" <<'PY'
import json, sys, os
path, conv = sys.argv[1], sys.argv[2]
data = {}
if os.path.isfile(path):
    with open(path) as f:
        data = json.load(f)
entry = data.get(conv, {"edits": 0, "gate_done": False})
entry["edits"] = int(entry.get("edits", 0)) + 1
data[conv] = entry
with open(path, "w") as f:
    json.dump(data, f)
PY
echo '{}'
exit 0
