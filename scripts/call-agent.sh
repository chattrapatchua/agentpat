#!/usr/bin/env bash
# Routine launch: ensure env (install only if missing), then open Cursor.
# Use --fresh to force a reinstall.
set -euo pipefail
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/common.sh"

case " $* " in
  *" --fresh "*) rm -f "$VENV/.installed"; ensure_env --force ;;
  *) ensure_env ;;
esac

open_cursor
