#!/usr/bin/env bash
# Rename the agent slug everywhere: agent/agent-name, Makefile targets, docs, and the
# root wrapper scripts (onboard-agent-<slug>, call-agent-<slug>, rename-agent-<slug>).
#
# Usage: bash scripts/rename-agent.sh <new-slug>
set -euo pipefail
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/common.sh"

NEW="${1:-}"
[ -n "$NEW" ] || { echo "Usage: bash scripts/rename-agent.sh <new-slug>" >&2; exit 1; }
[[ "$NEW" =~ ^[a-z0-9][a-z0-9-]*$ ]] || { echo "slug must be kebab-case: $NEW" >&2; exit 1; }

OLD="$(cat "$ROOT/agent/agent-name" 2>/dev/null | tr -d '[:space:]')"
[ -n "$OLD" ] || OLD="work-agent"
if [ "$OLD" = "$NEW" ]; then echo "already named '$NEW'." >&2; exit 0; fi

echo "[work-agent] renaming '$OLD' -> '$NEW'" >&2

# 1) slug source of truth
printf '%s\n' "$NEW" > "$ROOT/agent/agent-name"

# 2) command references in Makefile + docs
FILES=(
  "$ROOT/Makefile"
  "$ROOT/.cursor/MCP.md"
  "$ROOT/agent/mvp-cursor.md"
  "$ROOT/agent/IDE-ONBOARD.md"
  "$ROOT/agent/ide-target"
  "$ROOT/agent/ide-bootstrap/mcp/MCP.md"
)
for f in "${FILES[@]}"; do
  [ -f "$f" ] && sed -i "s/agent-$OLD/agent-$NEW/g; s/slug is $OLD/slug is $NEW/g" "$f"
done

# 3) rename root wrapper scripts
for verb in onboard call rename; do
  src="$ROOT/${verb}-agent-$OLD"
  dst="$ROOT/${verb}-agent-$NEW"
  [ -f "$src" ] && mv "$src" "$dst"
done

echo "[work-agent] done. New commands: ./onboard-agent-$NEW, ./call-agent-$NEW, make call-agent-$NEW" >&2
