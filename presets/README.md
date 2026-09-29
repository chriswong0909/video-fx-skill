# 風格預設（presets/SP-###）

**用途：** 一個預設 = 一套「字體 + 顏色意思 + 字級 + 緩動 + 轉場 + 字幕 + 調色 + 聲效家族 + 效果白名單」。
treatment（`workflow/director.md`）揀一個預設，全片所有效果都跟佢，咁先唔會每個效果各有各色。

| 預設 | 適合 | 調色 | 字幕 | 轉場 |
|---|---|---|---|---|
| SP-001 醫療專業 | 醫生口播、健康知識 | GR-001 | FX-051／FX-039 | FX-040 |
| SP-002 溫暖生活 | Vlog、生活建議 | GR-003 | FX-039 | FX-040、FX-042 |
| SP-003 活潑年輕 | 快節奏知識、產品 | GR-005 | FX-018／FX-052 | FX-046、FX-086 |
| SP-004 高級編輯感 | 品牌、訪問 | GR-007 | FX-039／FX-082 | FX-040、FX-077 |
| SP-005 新聞手作 | 新聞、解說 | GR-006 | FX-051 | FX-079、FX-040 |

## 每個預設有三個檔
- `preset.json`：機器讀（tokens、白名單、調色、聲效）
- `tokens.css`：放入 composition `<head>`，所有效果讀呢啲 CSS 變數
- `DESIGN.md`：人睇（色彩意思、唔好做嘅嘢）

## Token 標準（所有效果 snippet 用呢套名）
| Token | 用途 |
|---|---|
| `--c-bg` `--c-surface` `--c-text` | 背景、卡面、正文字 |
| `--c-accent` | 主強調色（每格最多一個強調色） |
| `--c-alert` | 警示／錯誤觀念 |
| `--c-positive` | 做法／正面 |
| `--c-caption-box` `--c-caption-text` | 字幕底同字 |
| `--f-display` `--f-body` `--f-num` | 標題、內文、數字字體（全片 ≤ 2 款） |
| `--fs-hero` 150 ／ `--fs-sub` 72 ／ `--fs-label` 64 ／ `--fs-caption` 80 ／ `--fs-foot` 52 | 字級（px，9:16） |
| `--ease-out` `--ease-pop` `--ease-move` `--ease-in` | 四款緩動（全片 ≤ 4 款） |
| `--dur-in` `--dur-out` `--dur-move` `--stagger` | 時間 |

效果 JS 用 `EASE.out / EASE.pop / EASE.move / EASE.in` 同 `DUR.in / DUR.out / DUR.move / DUR.stagger`
（snippet 開頭嘅 token 讀取器會由 CSS 變數讀，冇 tokens.css 就用返原本數值）。

## 用法
```html
<head>
  <style>/* 貼 presets/SP-001-medical-pro/tokens.css */</style>
  <style>/* 再貼品牌覆蓋（如有），例如 brands/medical-blue.md 嘅顏色 */ :root{--c-accent:#0099ce}</style>
</head>
```
優先次序：品牌檔 > 預設 > snippet 內嘅後備值。

## 檢查
```bash
node scripts/check-style.mjs work/index.html presets/SP-001-medical-pro
```
檢查：字體 ≤ 2、色相 ≤ 4、緩動 ≤ 4、轉場 ≤ 2、白名單、中文唔用大楷／斜體、字級下限、Math.random／repeat:-1。

## 新增預設
抄一個資料夾，改 `preset.json`，再行 `python3 scripts/presets.py build`（重出 tokens.css、DESIGN.md，同更新效果嘅 family 標籤）。
