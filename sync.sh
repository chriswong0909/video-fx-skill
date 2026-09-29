#!/bin/bash
# 同步效果庫：先下載 GitHub 最新版本，再上傳本機改動。
# 用法：喺終端機打  bash ~/Documents/GitHub/video-fx-skill/sync.sh
set -e
cd "$(dirname "$0")"
echo "① 下載 GitHub 最新版本…"
git pull --rebase --autostash origin main
echo "② 記錄本機改動…"
git add -A
if git diff --cached --quiet; then
  echo "   本機冇新改動"
else
  git commit -q -m "sync: $(date '+%Y-%m-%d %H:%M') $(hostname -s)"
fi
echo "③ 上傳到 GitHub…"
git push origin main
echo "✅ 同步完成"
