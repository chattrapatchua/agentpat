#!/usr/bin/env bash
# Shared helpers for the agent scripts. Sourced, not run directly.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV="$ROOT/.venv"

# Windows (Git Bash) puts the interpreter under Scripts/; POSIX under bin/.
# Resolve lazily — the layout is only known once the venv exists.
set_venv_py() {
  if [ -f "$VENV/Scripts/python.exe" ]; then
    VENV_PY="$VENV/Scripts/python.exe"
  else
    VENV_PY="$VENV/bin/python"
  fi
}
set_venv_py

# Pick a base python to create the venv with.
base_python() {
  if command -v python >/dev/null 2>&1; then echo "python";
  elif command -v python3 >/dev/null 2>&1; then echo "python3";
  else echo "ERROR: python not found on PATH" >&2; exit 1; fi
}

# Create the venv and install the project (editable) if needed.
# All setup output goes to stderr so callers that pipe stdout (e.g. MCP) stay clean.
ensure_env() {
  if [ ! -f "$VENV_PY" ]; then
    echo "[work-agent] creating virtualenv at .venv" >&2
    "$(base_python)" -m venv "$VENV" >&2
    set_venv_py   # layout is now known
  fi
  if [ ! -f "$VENV/.installed" ] || [ "${1:-}" = "--force" ]; then
    echo "[work-agent] installing dependencies (editable)…" >&2
    "$VENV_PY" -m pip install --upgrade pip >&2
    ( cd "$ROOT" && "$VENV_PY" -m pip install -e ".[dev]" ) >&2
    touch "$VENV/.installed"
  fi
}

open_cursor() {
  if command -v cursor >/dev/null 2>&1; then
    echo "[work-agent] opening Cursor…" >&2
    cursor "$ROOT" || true
  else
    echo "[work-agent] 'cursor' CLI not found — open the folder in Cursor manually:" >&2
    echo "  $ROOT" >&2
  fi
}
