---
name: video-fx
description: 用 HyperFrames 剪片、加動態字幕或模仿參考片效果時使用：必定先問三輪需求（品牌色、節奏、特別要求），出分鏡確認先生成素材同影片，剪完將新效果入庫。
---

# video-fx：會學習嘅剪片 skill（分鏡先行）

本 skill 係說明書；效果庫（資料）放喺使用者電腦：`~/Documents/GitHub/video-fx-skill/`（下稱 LIBRARY）。
效果目錄網頁：https://claude.ai/artifact/S4J778bzGTX56umuae9ZAQ

## 核心原則
1. **一定先問需求（硬性關卡）**：被召喚或收到素材後，第一件事係問三輪問題（見下面第 1 節）。未問完、未確認需求摘要之前，唔好轉錄、唔好分析、唔好出分鏡。
2. **分鏡先行，逐關確認（慳 token、慳 credits）**：未經使用者確認分鏡，唔好渲染、唔好生成素材。四個關卡，每關用 AskUserQuestion 問「確認／要改」：
   1. 分鏡：文字 + 效果庫預覽圖，唔渲染、唔生成
   2. 素材：列出要生成嘅素材同 credits，確認先生成
   3. 草稿：`--quality draft` 渲染一次，只睇一張細 contact sheet
   4. 正式版：`--quality high` 渲染 + 換原音軌 + 核對
   詳見 LIBRARY `workflow/storyboard.md`。

## 0. 連接效果庫（同問卷同步做，唔好因為讀檔而跳過問卷）
1. get_device_info 睇 connectedFolders；未有 `~/Documents` 或 LIBRARY，就用 device_request_folder_access 請求 `~/Documents/GitHub/video-fx-skill`。
2. device_bash 讀 `registry.json`（全部效果摘要、類別、配搭）、`lessons/*.md`（技術坑，必讀）、`brands/*.md`。
3. 需要時先讀 `workflow/*.md`、`effects/FX-###-*/effect.md`、`snippet.html`；只讀方案用到嗰幾個效果，唔好一次過讀晒。
4. 如果 LIBRARY 唔存在，照本檔流程做，並提醒使用者效果庫未搵到。

## 1. 開工問卷（強制，唔可以跳過）
即使使用者訊息已經講咗部分要求，都要問：已講嘅喺選項度預選或者寫明「你講咗 X，確認？」，未講嘅逐條問。只有使用者明確講「唔使問」或者「照你意思」先可以跳過，而且要喺需求摘要列明用咗咩預設。AskUserQuestion 唔可用時，用文字列出問題，然後停低等回覆。完整選項見 LIBRARY `workflow/intake.md`。

**第一輪：基本**（一次 AskUserQuestion，4 條）
1. 參考片：有（請提供）／冇，由你建議／有但只參考部分
2. 平台同長度：9:16 保持原長度／9:16 可剪短／16:9／1:1
3. 品牌色同字體：用 brands/ 現有品牌檔（列出名）／我提供色碼／跟參考片／由你建議
4. 字幕寫法：廣東話口語／書面語／英文／中英雙語

**第二輪：風格同節奏**
1. 節奏：快（1–2 秒一剪）／中（2–4 秒）／慢（保留講者，少剪）
2. 情緒：專業醫療／溫暖生活／活潑年輕／高級編輯感
3. 字幕密度：逐詞跳字／兩層重點字／只出重點字
4. 音樂同聲效：背景音樂 + 轉場聲效／只要轉場聲效／都唔要

**第三輪：素材同限制**
1. AI 生成素材：唔用／少量（例如 ≤ 20 credits）／可以放手用，出分鏡時報價
2. 講者出鏡：全程見到講者／可以用全屏過場蓋住講者
3. 開頭同結尾：要 hook 標題／要結尾 CTA／兩樣都要／都唔要
4. 特別要求或禁忌：自由填寫（例如唔要某顏色、要 logo、醫生名同職銜）

**問完**：輸出「需求摘要」表（項目｜答案），問一次「確認需求？」先進入第 2 節。節奏決定鏡頭長度同 cutaway 數量；情緒用嚟篩 registry 嘅 mood。

## 2. 分析（輕量）
- 有參考片：`bash scripts/analyze-ref.sh <ref.mp4> <out_dir>` → contact sheet、剪接點、靜音段。只將一張 sheet stage 去雲端用 Read 睇，逐段列：時間｜畫面｜手法｜類別｜FX-id 或 NEW。記錄色調（3–5 色碼）、字體、節奏、字幕位置，寫入 `refs/<slug>/analysis.md` + `sheet-small.jpg`（唔放原片）。只拆手法，唔抄受版權保護嘅素材本身。
- 冇參考片或參考片唔夠：由 registry.json 按 `fits`、`mood` 篩選。覆蓋規則：必須 1 × hook、1 × caption、1 × camera；15 秒以上加 1 × cutaway 或 list-chart；有列舉內容用 list-chart。檢查 `pairs_with`／`conflicts_with`。見 `workflow/recommend.md`。
- 轉錄：`tools/asr.py`（faster-whisper large-v3-turbo，language=yue，word timestamps）；低把握度字多數係口語位，要標示俾使用者核對。

## 3. 關卡一：分鏡
1. 按句切鏡頭（每鏡 1–4 秒），寫 `storyboards/<project>.json`（格式見 `storyboards/_example.json`）：每鏡時間、講緊咩、畫面描述、FX-id、素材（source：code／higgsfield／canva／client／footage）、生成描述、credits。
2. `node scripts/build-storyboard.mjs storyboards/<project>.json` → html；stage 去雲端，用 Artifact 發佈（同一專案重用同一連結）。
3. 問使用者確認；要改就只改 JSON 再 build，唔好重寫。

## 4. 關卡二：素材
- 見 `workflow/assets-higgsfield.md`。Higgsfield connector（`mcp__Higgsfield__*`，用 ToolSearch 載入）：generate_image、remove_background、generate_video、generate_3d、relight_image、upscale_*。Canva connector 做備用。
- 每個影片專案 `create_project` 一次，之後用同一個 folder_id；生成前一律 `get_cost:true` 預計 credits，列總數俾使用者確認先生成；多個素材用 batch + jobs_wait。
- 代碼做得到嘅（UI、圖表、線條、字幕、圖示輪廓）唔好用 AI 生成。醫學插圖 AI 生成要標明需醫生審核。冇真實素材時老實講明插圖會較扁平。

## 5. 關卡三、四：渲染
- 由 `snippet.html` 抄結構，改時間、文字、品牌色。
- 嚴守 lessons：
  - 全屏圖層（cutaway、畫廊、閃卡）一定要做 clip（data-start／data-duration／data-track-index），唔好只用 opacity，否則軟件渲染出黑塊
  - filter／transform 做喺 video 外層 wrapper，唔好做喺 video
  - 疊喺 #cam 上面嘅元素要有更高 z-index
  - 中文字體用 Google Fonts `&text=` 子集下載
  - 本機 VM（Linux ARM64）渲染要用 playwright chromium + libxdamage，見 lessons/hyperframes-rendering.md
  - device_bash 每次最多 180 秒，背景程序會被殺，長工作要拆段
- 草稿：`--quality draft` 渲染一次，睇一張細 contact sheet（每格 ≤ 300px）；只修出問題嘅段落，唔好反覆截圖。
- 正式版：`--quality high`；`ffmpeg -i render.mp4 -i source.mp4 -map 0:v:0 -map 1:a:0 -c copy out.mp4`，md5 核對音軌；核對長度、幀數、比例。
- 成品放素材旁邊 `output/`；HyperFrames 專案放 `~/Documents/GitHub/hyperframes-student-kit/video-projects/<name>/`。

## 6. 入庫（每次剪完都做）
1. 新效果：`node scripts/new-effect.mjs "<中文名>" <english-slug> <category>`，填 effect.md（front matter：id, name, name_en, category, tags, mood, fits, pairs_with, conflicts_with, needs, brand_color_ready, source, learned, used_in, difficulty；內文：效果、幾時用、幾時唔好用、參數同節奏、實作重點、已知限制）、snippet.html、preview.mp4（2–3 秒，闊 240px，crf 30）、preview.jpg（闊 360px）。
2. 用過或改良嘅效果：更新 effect.md，`used_in` 加今次專案。
3. 新技術坑寫入 `lessons/`；新品牌寫入 `brands/`。
4. `node scripts/build-registry.mjs` + `node scripts/build-gallery.mjs`，將 `gallery/artifact.html` 重新發佈到效果目錄同一連結。
5. 已連接資料夾入面 git 會因 lock 檔失敗：要 commit 就喺 VM scratch 做好再 rsync 入去。
6. 最後同使用者講：新增／更新咗邊啲效果（FX-id + 一句描述）。

## 類別
caption 字幕｜hook 開場｜camera 鏡頭｜cutaway 全屏過場｜list-chart 清單／卡片｜layout 版面｜transition 轉場｜grade-light 調色／補光｜accent 點綴｜sound 聲效

## 原則
- 用效果時註明 FX-id。
- 唔作假帳號、假數據、假認證剔號。
- 生成素材前一定講明 credits 同等確認。
- 同使用者溝通用廣東話，簡潔，新手友善。