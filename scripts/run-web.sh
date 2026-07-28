#!/usr/bin/env bash
# Run the web chat UI + API on http://127.0.0.1:8765
set -euo pipefail
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/common.sh"

ensure_env
echo "[work-agent] web chat → http://127.0.0.1:8765  (Ctrl-C to stop)" >&2
exec "$VENV_PY" "$ROOT/apps/web/server.py"
