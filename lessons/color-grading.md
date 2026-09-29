# 調色（grades/ 調色庫 + tools/grade.py）

## 原則
- **每條片都有基本調色**：按影片類型自動推薦（`python3 tools/grade.py recommend <影片類型> [情緒]`），使用者冇特別要求就用推薦；問卷入面寫明「推薦：GR-xxx」俾佢確認。
- 調色係「先校正、後風格」：`apply` 會先用中性像素做白平衡（只校正一半）同埋灰濛時拉黑白位，再套預設風格。
- **膚色優先**：膚色色相正常約 15–30°；調完用 `analyze` 再睇一次，超出範圍就減 `--strength`。膚色準唔準最後要使用者親眼確認。
- 醫療畫面（皮膚病、傷口、化驗、X 光）要準確顏色：用 GR-006 或 `--strength 0.5`，唔好用青橙、暗調。
- 手機 8-bit 片唔好大幅調（會出色帶）；風格太強就 `--strength 0.6–0.8`。

## 推薦表（grade.md 嘅 default_for／mood_zh）
| 影片類型／情緒 | 推薦 | 備選 |
|---|---|---|
| 醫療健康、口播知識、訪問對談、品牌企業 | GR-001 專業專訪 | GR-002 醫療清新（白色診所、藍色品牌）、GR-003 暖色 Podcast |
| 產品廣告 | GR-004 電影青橙 | GR-005 明亮生活 |
| 紀錄 Vlog | GR-005 明亮生活 | GR-003 |
| 新聞資訊、動畫解說 | GR-006 新聞中性 | — |
| 情緒：溫暖生活 | GR-003 | — |
| 情緒：活潑年輕 | GR-005 | — |
| 情緒：高級編輯感 | GR-004 或 GR-007 暗調編輯感 | — |
| B-roll 回憶／舊片感 | FX-074 復古菲林（只套 B-roll） | — |

## 流程
1. 分析：`python3 tools/grade.py analyze source.mp4` → 曝光、對比、白色位偏色、膚色；喺需求摘要講一句（例如「原片偏光、白牆微黃」）。
2. 分鏡關卡：`python3 tools/grade.py compare source.mp4 storyboards/<project>-grade.jpg GR-001 GR-002 GR-003` → 原片｜推薦｜備選 對比圖，一齊俾使用者確認。
3. 渲染前：`python3 tools/grade.py apply source.mp4 GR-001 graded.mp4 [--strength 0.8]` → HyperFrames 用 graded.mp4 做講者片（音軌 copy 不變，最後換原音軌時仍然用 source.mp4 音軌）。
4. 唔好喺 HyperFrames 再疊另一層調色 filter（除咗 B-roll 嘅 FX-074），避免重複調色。

## 新增調色預設
- `grades/GR-###-slug/grade.md`：front matter id, name, name_en, video_types, default_for, mood_zh, filters（ffmpeg 4.4 相容：curves、eq、colorchannelmixer、colorlevels、vignette；唔好用 huesaturation）、status。
- 跟參考片色調：由參考片抽幾格，對比 analyze 數據（曝光、飽和、光暗位偏色），寫 curves r/g/b 去接近；寫入新 GR 預設，source 寫 ref slug。
- `python3 tools/grade.py previews` 重做效果目錄預覽圖（樣本 `grades/_sample.mp4` 係使用者自己片段，唔入 git）。
