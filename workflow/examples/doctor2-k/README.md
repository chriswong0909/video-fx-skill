# doctor2 風格包版：專案腳本範例（2026-10-02）
用嚟抄嘅範本（路徑寫死 `~/hf/d2k`，新片要改）：
- `build.py`：讀 `storyboards/<project>-beats.json` → 逐拍 `cards.py use` → 砌 index.html（鏡頭表 CAM、skipcaps 收字幕、卡 host、品牌元素位置）。
- `sheet.sh 時間,時間 輸出.jpg`：逐拍截圖砌 contact sheet（自己先睇）。
- `page.py` + `page_tpl.html`：出節拍表頁（每拍截圖、卡、卡上字、聲效、字幕出唔出、畫面比例）。
- `sfx-events.json`：聲效落地時間 → `tools/sfx_plan.py` → `tools/sfx.py mix`。
- 分段 render：`tools/hf_chunk.py`。
