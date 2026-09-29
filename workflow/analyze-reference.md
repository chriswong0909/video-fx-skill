# 拆解參考片

## 步驟
1. `bash scripts/analyze-ref.sh ref.mp4 out/` → `out/sheet.jpg`（每 0.5 秒一格，有時間碼）、`out/cuts.txt`（剪接點）、`out/silence.txt`、`out/info.txt`
2. 睇 sheet.jpg（需要時用 Read 睇圖），逐段填下表：

| 時間 | 畫面類型 | 手法描述 | 類別 | 對應 FX / NEW |
|------|---------|---------|------|--------------|
| 0.0–1.3 | 講者 | 頂部頭像資料卡 + 兩層字幕 | hook, caption | FX-039, NEW |

3. 記錄整體語言：色調（取 3–5 個色碼）、字體風格、節奏（平均幾秒一剪）、轉場習慣、字幕位置。
4. 寫入 `refs/<slug>/analysis.md`，附 `sheet-small.jpg`（闊 ≤ 1200px，唔好放原片）。
5. 每個 NEW 手法 → 按 `add-effect.md` 開新效果。

## 注意
- 只拆「手法」，唔好抄受版權保護嘅素材本身（相片、logo、音樂）。
- 參考片用咗真實相片素材而我哋冇，要喺方案度講明會用插圖代替、效果會扁平啲。
