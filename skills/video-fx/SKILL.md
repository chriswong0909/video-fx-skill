---
name: "video-fx"
description: "用 HyperFrames 剪片、加動態字幕或模仿參考片效果時使用：必定先問三輪需求（品牌色、節奏、特別要求），出分鏡確認先生成素材同影片，按影片類型同節奏由效果庫、聲效庫同調色庫揀效果（自動推薦基本調色），渲染前做字級、字幕、面部禁區檢查，剪完入庫並同步 GitHub。"
---

# video-fx：會學習嘅剪片 skill（分鏡先行）

本 skill 係說明書；效果庫（資料）放喺使用者電腦：`~/Documents/GitHub/video-fx-skill/`（下稱 LIBRARY，已同 GitHub 同步）。
效果目錄網頁（視覺效果、聲效、調色三個分頁）：https://claude.ai/artifact/S4J778bzGTX56umuae9ZAQ

## 核心原則
1. **一定先問需求（硬性關卡）**：被召喚或收到素材後，第一件事係問三輪問題（第 1 節）。未問完、未確認需求摘要之前，唔好轉錄、唔好分析、唔好出分鏡。
2. **分鏡先行，逐關確認**：未經使用者確認分鏡，唔好渲染、唔好生成素材。四個關卡，每關用 AskUserQuestion 問「確認／要改」：
   1. 分鏡：文字 + 效果庫預覽圖，唔渲染、唔生成
   2. 素材：列出要生成嘅素材、來源同額度，確認先生成
   3. 草稿：`--quality draft` 渲染一次，只睇一張細 contact sheet
   4. 正式版：`--quality high` 渲染 + 換原音軌 + 核對
   詳見 LIBRARY `workflow/storyboard.md`。

**硬性規則（每條片都要遵守，詳見 `lessons/layout-safety.md`）**
- **字幕只得一種**：全片揀一款基本字幕，FX-039（白字 + 黑光暈，80px，按意群 6–12 字，單行）為預設，或者 FX-051 方框字幕，二揀一唔好混用。字幕入面唔准換色、反白；有特效字顯示緊嗰句，嗰句唔出字幕。
- **最細字**（1080×1920）：特效大字 150px、特效細字 72px、標籤／膠囊 64px、字幕 80px、註腳 52px；大細字比例 ≤ 2.5。snippet 數值低過準則一律以準則為準。
- **面部禁區**：特效字唔准遮面；每鏡按推鏡倍數計面部位置，渲染前自動檢查重疊。
- **唔加未要求嘅元素**：效果庫冇、用戶又冇要求嘅嘢（進度條、水印等）預設唔加；要加就喺確認問題逐項問。
- **素材唔好靜靜雞降級**：效果需要相片時按 `workflow/assets.md` 次序（Canva 第一）；跌到代碼插圖要先講明。
- **禁用／移除效果**：`status: banned` 唔好推薦、唔好用，除非用戶主動要求。`effects/REMOVED.md` 列出嘅 ID（FX-001、002、007、008、009、011、012）已刪除，唔好再用、唔好重用編號。
- **節奏同機位**（詳見 `lessons/rhythm-variety.md`）：單機位口播用固定三機位（闊 1.0／中 1.3／特寫 1.7，#cam wrapper 縮放），眼睛高度一致；相連講者鏡頭倍數差 ≥ 1.3、硬切相隔 ≥ 1.5 秒、切喺停頓位；重點位用 FX-040 平滑推鏡。
- **開場**：0.1 秒內出字、停最少 2.5 秒、最少 150px，內容係全片問題或結論。
- **唔准靜止**：任何 ≥ 1 秒嘅靜止段都要加慢推或浮動；全屏效果第一個元素出現前唔好有超過 0.3 秒空白。
- **多樣性**：同一效果每 60 秒最多 2 次、相隔 ≥ 15 秒；「頭頂大字」類畫面全片最多 3 次；優先用未用過而又適合嘅效果。
- **基本調色（每條片都要）**：按影片類型／情緒推薦調色預設（`python3 tools/grade.py recommend <影片類型> [情緒]`，例如醫生口播 → GR-001 專業專訪）；使用者冇特別要求就用推薦，有要求（跟參考片、保持原色、指定風格）就跟佢。膚色優先，醫療顏色（皮膚、傷口）要準。詳見 `lessons/color-grading.md`。

## 0. 連接效果庫（同問卷同步做，唔好因為讀檔而跳過問卷）
1. get_device_info 睇 connectedFolders；未有 `~/Documents` 或 LIBRARY，就用 device_request_folder_access 請求 `~/Documents/GitHub/video-fx-skill`。
2. device_bash 讀 `registry.json`（效果摘要、類別、video_types、pace、配搭、status、cjk_fit；`sounds` 陣列係聲效庫、`grades` 陣列係調色庫）、`lessons/*.md`（技術坑同版面規則，必讀）、`brands/*.md`。
3. 需要時先讀 `workflow/*.md`、`effects/FX-###-*/effect.md`、`snippet.html`；只讀方案用到嗰幾個效果，唔好一次過讀晒。
4. **LIBRARY 攞唔到（例如喺網頁版 Claude）**：用 Artifact 工具 `action: read` 讀效果目錄網頁，入面 `<script id="fxdata">` 有全部效果 JSON。唔好當冇效果庫、唔好由零設計效果。提醒使用者：入庫要喺有 LIBRARY 嘅環境做。

## 1. 開工問卷（強制，唔可以跳過）
即使使用者已經講咗部分要求，都要問：已講嘅喺選項預選或寫明「你講咗 X，確認？」，未講嘅逐條問。只有使用者明確講「唔使問」或者「照你意思」先可以跳過，並喺需求摘要列明用咗咩預設（保留原聲、原長度、原比例；字幕跟講者語言；講者出現約 60–80%）。AskUserQuestion 唔可用時，用文字列出問題，然後停低等回覆。完整選項見 `workflow/intake.md`。

**第一輪：基本**
1. 參考片：有（請提供）／冇，由你建議／有但只參考部分
2. 平台同長度：9:16 保持原長度／9:16 可剪短／16:9／1:1
3. 品牌色同字體：用 brands/ 現有品牌檔（列出名）／我提供色碼／跟參考片／由你建議
4. 字幕寫法：廣東話口語／書面語／英文／中英雙語（有冇講稿）

**第二輪：類型、風格同節奏**
1. 影片類型：口播知識／訪問對談／醫療健康／動畫解說／產品廣告／紀錄 Vlog／新聞資訊／品牌企業
2. 節奏：快（1–2 秒一剪）／中（2–4 秒）／慢（4 秒以上，少剪）
3. 情緒：專業醫療／溫暖生活／活潑年輕／高級編輯感
4. 字幕款式同音樂：FX-039 光暈字幕或 FX-051 方框字幕；背景音樂 + 聲效／只要聲效（由 sounds/ 聲效庫揀）／都唔要

**第三輪：素材同限制**
1. AI 生成素材：唔用／少量（例如 ≤ 20 credits）／可以放手用，出分鏡時報價
2. 講者出鏡：全程見到講者／可以用全屏過場蓋住講者
3. 開頭同結尾：要 hook 標題／要結尾 CTA／兩樣都要／都唔要
4. 特別要求或禁忌：自由填寫（例如唔要某顏色、要 logo、醫生名同職銜、需唔需要補光調色）

**問完**：輸出「需求摘要」表（項目｜答案），入面一定有「調色」一行：寫推薦預設（例如「GR-001 專業專訪（按醫療健康推薦）」）；使用者喺特別要求講過顏色就跟佢。問一次「確認需求？」先進入第 2 節。

## 2. 分析（輕量）
- 有參考片：`bash scripts/analyze-ref.sh <ref.mp4> <out_dir>` → contact sheet、剪接點、靜音段。只將一張 sheet stage 去雲端用 Read 睇，逐段列：時間｜畫面｜手法｜類別｜FX-id 或 NEW。記錄色調（3–5 色碼）、字體、節奏、字幕位置，寫入 `refs/<slug>/analysis.md` + `sheet-small.jpg`（唔放原片）。只拆手法，唔抄受版權保護嘅素材本身。
- **參考片係英文（或非中文）**：每個有文字嘅手法按 `lessons/cjk-adaptation.md` 清單檢查，analysis.md 每段加「中文適應：good／adjust／poor + 要改咩」。用中文實際內容試渲染一格，縮到 360px 闊睇得清先算數。
- 揀效果：由 registry.json 按 `video_types`、`pace`（跟問卷答案）再按 `fits`、`mood` 篩選；排除 banned 同 REMOVED；`cjk_fit: poor` 預設唔推薦，優先 good。覆蓋規則：1 款基本字幕 + 1 個開場手法 + 1 × camera；15 秒以上加 1 × cutaway 或 list-chart；有列舉內容用 list-chart。檢查 `pairs_with`／`conflicts_with`。見 `workflow/recommend.md`。
- 調色分析：`python3 tools/grade.py analyze source.mp4` → 曝光、白色位偏色、膚色；有問題（偏暗、偏黃、膚色唔自然）喺分鏡講一句。
- 轉錄：`tools/asr.py`（faster-whisper large-v3-turbo，language=yue，word timestamps）；低把握度字多數係口語位，要標示俾使用者核對。亂碼或重複段用 `condition_on_previous_text=False` 分段重轉。

## 3. 關卡一：分鏡
1. 按句切鏡頭（每鏡長度跟節奏答案），寫 `storyboards/<project>.json`（格式見 `storyboards/_example.json`）：每鏡時間、講緊咩、畫面描述、FX-id、**字幕模式（基本字幕／由特效字取代，並寫出特效字）**、素材（source：canva／footage／higgsfield／stock／code）、生成描述、額度；要聲效就加 `sfx`（`[{"sfx":"SFX-001","t":3.8}]`，按效果嘅配搭聲效揀），分鏡網頁可以試聽。
2. `node scripts/build-storyboard.mjs storyboards/<project>.json` → html；stage 去雲端，用 Artifact 發佈（同一專案重用同一連結）。JSON 頂層加 `"grade": "GR-001"`；另外出調色對比圖 `python3 tools/grade.py compare source.mp4 storyboards/<project>-grade.jpg <推薦> <備選1> <備選2>`，同分鏡一齊俾使用者確認。
3. 確認問題逐項列出：效果庫以外嘅元素、`cjk_fit: adjust` 效果要改嘅參數、講者出現比例、每個效果用咗幾次、有冇類別缺可用效果。
4. 問使用者確認；要改就只改 JSON 再 build，唔好重寫。

## 4. 關卡二：素材
- 按 `workflow/assets.md` 次序：**Canva → 原片截圖 → Higgsfield → 有授權圖庫 → 代碼插圖**。
- Canva connector（`mcp__Canva__*`，用 ToolSearch 載入）：generate-image（9:16 用 PORTRAIT_9_16）、用戶已有素材。
- Higgsfield connector（`mcp__Higgsfield__*`）：每個專案 `create_project` 一次；生成前一律 `get_cost:true`，列總數確認先生成；多個素材用 batch + jobs_wait。詳見 `workflow/assets-higgsfield.md`。
- 代碼做得到嘅（UI、圖表、線條、字幕、圖示輪廓）唔好用 AI 生成；但效果 `needs` 要相片嘅，唔好用代碼插圖頂替而唔講。醫學插圖一律標明需醫生審核。

## 5. 關卡三、四：渲染
- 渲染前先調色：`python3 tools/grade.py apply source.mp4 <GR-id> graded.mp4 [--strength 0.8]`，HyperFrames 講者片用 graded.mp4（音軌照用 source.mp4）；唔好喺 HyperFrames 再疊調色 filter（B-roll 嘅 FX-074 除外）。
- 由 `snippet.html` 抄結構，改時間、文字、品牌色；**位置同字級唔好照抄**：位置按面部禁區重排，字級按最細字準則同 `cjk_notes` 調整。
- 嚴守 lessons：
  - 全屏圖層（cutaway、畫廊、閃卡）一定要做 clip（data-start／data-duration／data-track-index），唔好只用 opacity，否則軟件渲染出黑塊
  - filter／transform 做喺 video 外層 wrapper，唔好做喺 video
  - 疊喺 #cam 上面嘅元素要有更高 z-index
  - 中文字體用 Google Fonts `&text=` 子集下載
  - 本機 VM（Linux ARM64）渲染要用 playwright chromium + libxdamage，見 lessons/hyperframes-rendering.md
  - device_bash 每次最多 180 秒，背景程序會被殺，長工作要拆段
- **渲染前自動檢查**（`lessons/layout-safety.md` 第 6 節）：字級、字幕字數、面部禁區、機位差距、多樣性五項全過先出草稿。
- **草稿後動態檢查**（`lessons/rhythm-variety.md` 第 6 節）：`motion.py` 冇任何 ≥ 1 秒靜止段先出正式版。
- 草稿：`--quality draft` 渲染一次，睇一張細 contact sheet（每格 ≤ 300px）；只修出問題嘅段落。
- 正式版：`--quality high`；冇聲效：`ffmpeg -i render.mp4 -i source.mp4 -map 0:v:0 -map 1:a:0 -c copy out.mp4`，md5 核對音軌。有聲效：`python3 tools/sfx.py mix source.mp4 cues.json mix.m4a` 再 mux（原聲音量不變 + limiter），並講明音軌已加聲效。核對長度、幀數、比例。
- 成品放素材旁邊 `output/`；HyperFrames 專案放 `~/Documents/GitHub/hyperframes-student-kit/video-projects/<name>/`。

## 聲效（詳見 `lessons/sound-mixing.md`）
- 聲效庫喺 `sounds/SFX-###-slug/`（sound.md + sound.mp3），編號同 FX 分開。揀聲效睇 registry.json 嘅 `sounds`：按 `pairs_with`（配邊個 FX）、`pace`、`mood`。
- 落聲對準畫面動作（出現格／接觸格），唔係句子開頭；口播片每 3–5 秒最多 1 個，ding 全片 1–3 次；講者講重點字嗰刻唔落大聲效。
- 新聲效：內置合成 `python3 tools/sfx.py synth`；外來免版稅聲效 `python3 tools/sfx.py add ...`，授權唔清楚唔入庫。唔好由參考片抽聲效，參考片只記錄幾時落聲。

## 6. 入庫（每次剪完都做）
1. 新效果：`node scripts/new-effect.mjs "<中文名>" <english-slug> <category>`（編號自動取最大 +1，唔會重用已移除編號），填 effect.md front matter：id, name, name_en, category, tags, mood, fits, **video_types, pace**, pairs_with, conflicts_with, needs, brand_color_ready, source, learned, used_in, difficulty, **status, cjk_fit, cjk_notes, placement**；內文：效果、幾時用、幾時唔好用、參數同節奏、實作重點、已知限制。另加 snippet.html、preview.mp4（2–3 秒，闊 240px，crf 30）、preview.jpg（闊 360px）。
   - 由非中文參考學返嚟：`cjk_fit` 必填；snippet 參數以中文版為準，英文原值寫入 `cjk_notes`。
   - 有文字嘅效果：`placement` 必填（headroom／lower／center／free／inline／layout／behind-subject）；會疊喺講者身上嘅加 `needs: face-box`。
2. 用過或改良嘅效果：更新 effect.md，`used_in` 加今次專案。
3. 用戶否定：
   - 講「唔啱／唔好用」→ 改 `status: banned` + `banned_reason`（邊條片、點解），唔刪。
   - 明確講「移除／刪除」→ 將資料夾搬去 `../_to_delete/removed_effects/`，喺 `effects/REMOVED.md` 記錄 ID、日期、原因；編號永不重用。
   - 只係某條片唔啱用 → 唔好禁用。
4. 新技術坑寫入 `lessons/`；新品牌寫入 `brands/`；用過嘅聲效喺 sound.md、用過嘅調色喺 grade.md 嘅 `used_in` 加專案；跟參考片調出嘅新色調寫成新 `grades/GR-###-slug/grade.md`。
5. `node scripts/build-registry.mjs` + `node scripts/build-gallery.mjs`，將 `gallery/artifact.html` 重新發佈到效果目錄同一連結（被拒就讀返網上最新版合併再發佈）。
6. 同步 GitHub（repo：`chriswong0909/video-fx-skill`，branch `main`）：
   - 先喺本機 commit：device_bash `cd LIBRARY && git add -A && git commit -m "..."`（行完確認冇 `.git/*.lock`、`tmp_obj_*` 殘留；有就刪，唔夠權限就用 device_request_delete_permission）。
   - **只改文字檔**（.md/.json/.html/.mjs/.py/.sh）：再用 GitHub MCP（`mcp__remote-devices__github__push_files`，用 ToolSearch 載入）將同一批檔案、同一句 commit message 推上 `main`。推完用 `get_file_contents` 對比遠端 blob sha 同本機 `git hash-object`，一致先算成功（內容一致，本機同步時 git 會自動略過重複 commit）。
   - **有二進制檔**（preview.mp4、preview.jpg、sound.mp3 等，GitHub MCP 推唔到）：唔好用 MCP 推，提醒使用者喺 Finder 雙擊 `Documents/GitHub/video-fx-skill/推上GitHub.command`，完成後用 `list_commits` 核對。
   - 永遠唔好問使用者攞 token／密碼。
7. 最後同使用者講：新增／更新／禁用／移除咗邊啲效果（FX-id + 一句描述），同埋 GitHub 已推送定係要佢雙擊同步檔。

## 類別
caption 基本字幕（FX-039／FX-051 呢類）｜text-fx 特效字｜hook 開場｜camera 鏡頭｜cutaway 全屏過場｜list-chart 清單／卡片｜layout 版面｜transition 轉場｜grade-light 調色／補光｜accent 點綴（聲效唔入 effects，放 sounds/）

## 原則
- 用效果時註明 FX-id。
- 唔作假帳號、假數據、假認證剔號；示意圖要標明「示意」。
- 生成素材前一定講明額度或 credits 同等確認。
- 同使用者溝通用廣東話，簡潔，新手友善。
