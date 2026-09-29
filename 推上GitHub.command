#!/bin/bash
# 雙擊呢個檔就會同步 video-fx 效果庫去 GitHub（用你 Mac 已登入嘅 git）
cd "$(dirname "$0")"
rm -f .git/index.lock
echo "== 同步 video-fx-skill =="
bash ./sync.sh && echo "" && echo "✅ 完成，已推上 GitHub。可以關閉呢個視窗。" || echo "❌ 有問題，請截圖俾 Claude 睇。"
read -n 1 -s -r -p "按任意鍵關閉…"
