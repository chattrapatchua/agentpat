#!/usr/bin/env bash
# First-time setup: create venv, install, then open Cursor (unless --no-open).
set -euo pipefail
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/common.sh"

ensure_env --force

if [ ! -f "$ROOT/.env" ] && [ -f "$ROOT/.env.example" ]; then
  cp "$ROOT/.env.example" "$ROOT/.env"
  echo "[work-agent] created .env from .env.example — add a model key to use the web chat." >&2
fi

echo "[work-agent] setup complete." >&2
echo "  Cursor MCP: enable 'work-agent' under Settings → MCP (starts via .cursor/mcp.json)." >&2
echo "  Web chat:   bash scripts/run-web.sh   →  http://127.0.0.1:8765" >&2

case " $* " in
  *" --no-open "*) : ;;
  *) open_cursor ;;
esac
