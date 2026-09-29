# 新效果入庫

## ID 規則
`FX-###` 順序編號，永不重用。資料夾名：`FX-###-english-slug`。

## 開新效果
```
node scripts/new-effect.mjs "兩層金色斜體字幕" two-tier-gold-caption caption
```
會建立 `effects/FX-###-slug/`，入面有 `effect.md` 範本同空白 `snippet.html`。

## effect.md 欄位（YAML front matter）
| 欄位 | 說明 |
|------|------|
| id, name, name_en | 編號、中文名、英文 slug |
| category | 見 SKILL.md 類別 |
| tags | 自由標籤 |
| mood | warm / clinical / editorial / energetic / premium / playful … |
| video_types | 影片類型：口播知識、訪問對談、醫療健康、動畫解說、產品廣告、紀錄 Vlog、新聞資訊、品牌企業（可多選） |
| pace | 節奏：快（1–2 秒一剪）、中（2–4 秒）、慢（4 秒以上），可多選 |
| fits | 適合內容：talking-head, podcast-clip, medical, product, education … |
| pairs_with / conflicts_with | 其他 FX-id |
| needs | 前置條件：word-timestamps, photo-assets, matting … |
| brand_color_ready | true = 顏色用 CSS 變數，可直接套品牌色 |
| source | 出處（ref slug + 時間）或 original |
| learned | 日期 |
| used_in | 用過嘅專案 |
| difficulty | easy / medium / hard |

內文：效果描述、幾時用、幾時唔好用、參數同節奏、實作重點、已知限制。

## snippet.html
- 可直接貼入 HyperFrames composition 嘅片段：CSS + HTML + GSAP（`tl` 由外面提供）。
- 時間用變數（例如 `T0`），顏色用 CSS 變數。
- 開頭註明依賴（字體、素材）。

## preview.jpg
由成品抽一格，闊 360px。

## 完成後
`node scripts/build-registry.mjs`，然後提醒使用者 Commit + Push。

## 更新效果目錄網頁
1. 每個效果要有 `preview.mp4`（2–3 秒，闊 240px，無聲，`-crf 30`）同 `preview.jpg`。
2. `node scripts/build-gallery.mjs` → `gallery/artifact.html`（Artifact 用）同 `gallery/index.html`（本機開）。
3. 用 Artifact 工具重新發佈到**同一條連結**：`url: https://claude.ai/artifact/S4J778bzGTX56umuae9ZAQ`（檔案要先 stage 去雲端 workspace）。
