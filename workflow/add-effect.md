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
