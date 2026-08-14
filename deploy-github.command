#!/bin/bash

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
PROJECT_DIR="$SCRIPT_DIR"
cd "$PROJECT_DIR"

if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "This folder isn't connected to GitHub yet (no git init / no remote set)."
    echo "Run this once first:"
    echo "  git init"
    echo "  git remote add origin <your GitHub repo URL>"
    echo "  git branch -M main"
    echo ""
    echo "Press Enter to close..."
    read
    exit 1
fi

echo "What did you change? (Press Enter when done)"
read msg

if [ -z "$msg" ]; then
    echo "Commit message cannot be empty. Aborting."
    read
    exit 1
fi

git add .
if git diff --cached --quiet; then
    echo "No new changes to commit, pushing existing content..."
else
    git commit -m "$msg" || { echo "Commit failed, aborting. Nothing was deployed."; read; exit 1; }
fi

if git push -u origin main; then
    echo "Deployed!"
else
    echo "Push failed, nothing was actually deployed. Check the error above."
fi

echo ""
echo "Press Enter to close..."
read
