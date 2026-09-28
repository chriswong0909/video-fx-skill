---
name: video-fx
description: 用 HyperFrames 剪片／做動態字幕時使用。收到影片素材、參考片（ref）、或被要求「模仿某條片嘅效果」、「幫我剪片」、「加字幕／特效」時觸發。會先問清楚需求，拆解參考片效果，由效果庫（effects/）揀選同組合效果，剪完將新學到嘅效果寫返入庫。
---

# video-fx：會學習嘅剪片 skill

呢個 skill 分兩部分：
- **本檔（說明書）**：點問、點分析、點揀效果、點入庫。
- **效果庫（資料）**：`effects/`、`registry.json`、`brands/`、`refs/`、`lessons/`，會不斷增長。

## 0. 搵效果庫（LIBRARY_ROOT）

每次開工先搵效果庫，用最新版本：
1. `~/Documents/GitHub/video-fx-skill/`（使用者本機 clone，最新）
2. 如果冇，用本檔往上兩層（`skills/video-fx/../../`）
3. 都冇，就喺 GitHub `chriswong0909/video-fx-skill` 讀（私人 repo 需要使用者本機 clone）

搵到後讀：`registry.json`（全部效果摘要）、`lessons/`（技術坑，必讀）、相關 `brands/`。

## 1. 開工問卷（見 `workflow/intake.md`）

收到素材或被召喚時，**先問，唔好即刻剪**。用 AskUserQuestion，一次最多 4 條，優先問：
1. 有冇參考片？（有 → 走第 2 步；冇 → 走第 3 步）
2. 平台同尺寸、目標長度（可否剪短？原聲要唔要全程保留？）
3. 品牌色／字體／品牌檔（`brands/` 有就直接揀）
4. 字幕語言同寫法（廣東話口語／書面語／英文），有冇講稿

之後按需要再追問：素材（B-roll、相、logo）、嚴格程度（「貼足 ref」定「參考 ref 再自由發揮」）、禁忌。使用者冇講嘅，用合理預設並講明。

## 2. 有參考片：拆解效果（見 `workflow/analyze-reference.md`）

1. 跑 `scripts/analyze-ref.sh <ref.mp4> <out_dir>`：出 contact sheet、剪接點、靜音段。
2. 睇 contact sheet，逐段列出用咗咩手法（時間、類別、描述）。
3. 對照 `registry.json`：每個手法標記為 **已有（FX-xxx）** 或 **新效果**。
4. 將分析寫入 `refs/<ref-slug>/analysis.md`（附 contact sheet 細圖，唔好放原片）。

## 3. 冇參考片／參考片效果唔夠：建議組合（見 `workflow/recommend.md`）

按內容類型（`fits`）、情緒（`mood`）、類別覆蓋，由 registry 揀一套組合：每條片最少要有 1 個 caption、1 個 camera、1 個 hook；長過 15 秒建議加 1 個 cutaway 或 list-chart。檢查 `pairs_with` / `conflicts_with`。出方案表俾使用者揀。

## 4. 出方案 → 確認 → 剪

方案表格式：時間段｜講緊咩｜用邊個效果（FX-id）｜備註。使用者確認先開始。
剪片時：
- 由 `effects/FX-xxx/snippet.html` 抄結構，改時間同文字，套用品牌色。
- 嚴守 `lessons/` 入面嘅技術規則（例如全屏圖層要用 data-start 做 clip，唔好只用 opacity）。
- 原聲：出片後用 `ffmpeg -map 0:v -map 1:a -c copy` 換返原音軌，並核對音軌 md5。
- 驗證：長度、幀數、比例、音軌；抽 contact sheet 親自睇。

## 5. 入庫（每次剪完都做）

見 `workflow/add-effect.md`：
1. 新效果：`node scripts/new-effect.mjs "<中文名>" <english-slug> <category>` → 填 `effect.md`、`snippet.html`、`preview.jpg`。
2. 舊效果有改良：更新該 `effect.md`，`used_in` 加今次專案。
3. 新技術坑寫入 `lessons/`。
4. `node scripts/build-registry.mjs` 重建 registry。
5. 話俾使用者知新增咗咩，提醒佢喺 GitHub Desktop Commit + Push。

## 類別（category）
`caption` 字幕／動態文字｜`hook` 開場｜`camera` 鏡頭運動｜`cutaway` 全屏過場｜`list-chart` 清單／圖表／卡片｜`layout` 版面｜`transition` 轉場｜`grade-light` 調色／補光｜`accent` 小裝飾｜`sound` 聲效

## 原則
- 效果庫係事實來源：用效果時註明 FX-id，方便日後追蹤。
- 唔可以扮真：唔作假帳號、假數據、假認證。
- 聽唔到聲：字幕由 ASR 出，要標明需要人手核對嘅字。
