#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
PROJECT_DIR="$SCRIPT_DIR"
cd "$PROJECT_DIR"

PYTHON_BIN="${PYTHON_BIN:-python3}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    echo "Python not found: $PYTHON_BIN"
    read "?Press Return to close..."
    exit 1
fi

if ! "$PYTHON_BIN" -c "import webview" >/dev/null 2>&1; then
    echo "pywebview is not installed."
    echo "Install it with: $PYTHON_BIN -m pip install pywebview"
    read "?Press Return to close..."
    exit 1
fi

exec "$PYTHON_BIN" app.py
