#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
WORKER_DIR="$SCRIPT_DIR/cloudflare"

if [[ ! -d "$WORKER_DIR" ]]; then
  echo "找不到 cloudflare 資料夾。"
  exit 1
fi

cd "$WORKER_DIR"

echo "正在部署 HamsterGo Cloudflare Worker..."
echo "如果顯示未登入，請先執行：npx wrangler login"
echo ""

npx wrangler deploy

echo ""
echo "Worker 部署完成。"
if [[ -t 0 ]]; then
  read -r "?按 Enter 關閉..."
fi
