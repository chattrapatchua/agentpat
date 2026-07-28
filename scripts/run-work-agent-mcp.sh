#!/usr/bin/env bash
# Started by Cursor via .cursor/mcp.json. stdout is the MCP channel — keep it clean.
set -euo pipefail
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/common.sh"

ensure_env            # setup logs go to stderr, never stdout
exec "$VENV_PY" -m mcp_server.server
