#!/usr/bin/env bash
# Run the agent-core test suite.
set -euo pipefail
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/common.sh"

ensure_env
exec "$VENV_PY" -m pytest "$ROOT/tests" -q
