# 40S：訪問片專案腳本範例（2026-10-03）
兩人闊鏡訪問、冇舊主檔，index.html 由零砌。路徑用環境變數 `FXLIB`（技能庫）同腳本所在資料夾（專案）。
- `build.py`：讀 `storyboards/40s-beats.json` → 逐拍 `cards.py use`（每拍可以揀品牌色版本，例如 `fin-channel:warm`）→ 砌 index.html（鏡頭表 CAM、光暈字幕、skipcaps、卡 host、manifest 每個字對返自己嘅 cue）→ 下載字型子集。
- `sheet.sh 時間,時間 輸出.jpg`：逐拍截圖砌 contact sheet。
- `page.py` + `page_tpl.html`：出節拍表頁。
- 假機位：單機位闊鏡用 `#camInner` 推近（transform-origin 0 0；[scale, x, y]），主持／嘉賓各一個 1.45 倍構圖；上圖下人用 y +330。
