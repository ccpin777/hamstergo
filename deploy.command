#!/bin/bash

cd "$(dirname "$0")"

if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "這個資料夾還沒有連接 GitHub（沒有執行過 git init / 沒有設定 remote）。"
    echo "請先手動執行一次："
    echo "  git init"
    echo "  git remote add origin <你的 GitHub repo 網址>"
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

latest_tag=$(git tag --sort=-version:refname | head -1)
if [ -n "$latest_tag" ]; then
    echo "Current latest version: $latest_tag"
fi
echo "Tag this version? (e.g. 1.0) — Press Enter to skip"
read tag

git add .
if git diff --cached --quiet; then
    echo "沒有新的變更可以 commit，直接 push 現有的內容..."
else
    git commit -m "$msg" || { echo "Commit 失敗，已中止，沒有部署。"; read; exit 1; }
fi

if [ -n "$tag" ]; then
    git tag "v$tag"
    if git push -u origin main --tags; then
        echo "Deployed and tagged as v$tag!"
    else
        echo "Push 失敗，沒有真的部署成功，請檢查上面的錯誤訊息。"
    fi
else
    if git push -u origin main; then
        echo "Deployed!"
    else
        echo "Push 失敗，沒有真的部署成功，請檢查上面的錯誤訊息。"
    fi
fi

echo ""
echo "Press Enter to close..."
read
