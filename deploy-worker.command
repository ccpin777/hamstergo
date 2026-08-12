#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
WORKER_DIR="$SCRIPT_DIR/cloudflare"

if [[ ! -d "$WORKER_DIR" ]]; then
  echo "cloudflare directory not found."
  exit 1
fi

cd "$WORKER_DIR"

echo "Deploying the HamsterGo Cloudflare Worker..."
echo "If Wrangler reports that you are not logged in, run: npx wrangler login"
echo ""

npx wrangler deploy

echo ""
echo "Worker deployment complete."
if [[ -t 0 ]]; then
  read -r "?Press Enter to close..."
fi
