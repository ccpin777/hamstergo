#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
PROJECT_DIR="$SCRIPT_DIR"
cd "$PROJECT_DIR"

WORKSPACE_DIR=$(cd "$SCRIPT_DIR/../.." && pwd)
PYTHON_BIN="${PYTHON_BIN:-$WORKSPACE_DIR/venv/bin/python}"

if [ ! -x "$PYTHON_BIN" ]; then
    echo "Python not found: $PYTHON_BIN"
    read "?Press Return to close..."
    exit 1
fi

if ! "$PYTHON_BIN" -c "import webview" >/dev/null 2>&1; then
    echo "pywebview is not installed."
    echo "Run $WORKSPACE_DIR/system/setup_venv.command first."
    read "?Press Return to close..."
    exit 1
fi

exec "$PYTHON_BIN" app.py
