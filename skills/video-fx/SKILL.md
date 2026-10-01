---
name: "video-fx"
description: "用 HyperFrames 剪片、加動態字幕、插 B-roll 動態圖像或模仿參考片效果時使用：必定先問三輪需求（品牌色、節奏、特別要求），剪停頓同口頭禪，參考片先拆成風格指南，出導演 treatment + 動態系統卡確認，再出分鏡、節拍表同關鍵格靜圖確認先 render，按影片類型同節奏由效果庫、聲效庫同調色庫揀效果（自動推薦基本調色），渲染前做 QA（字對聲、版面、一致性）同自評分，剪完入庫並同步 GitHub。"
---

# video-fx：會學習嘅剪片 skill（導演核心 + 模式）

## 結構：一個導演核心 + 四個模式
核心流程（本檔）所有片都行；模式只補該類片獨有嘅步驟，喺 LIBRARY `modes/`：
| 模式 | 用喺 | 檔 |
|---|---|---|
| A 真人口播剪片 | 醫生片、講者片（預設） | `modes/talking-head.md` |
| B B-roll 動態插片 | 真人片入面插動態圖像（全屏 cutaway／講者縮邊 + 透明板） | `modes/broll.md` |
| C 無真人講解片 | 旁白 + 全動態／生成鏡頭 | `modes/explainer.md` |
| D 產品／品牌宣傳 | 由網址、UI 截圖做宣傳片 | `modes/promo.md` |

```
問卷 → 轉錄 + 剪停頓 → (參考片 → 風格指南) → ★Treatment + 動態系統卡★ → ★分鏡★ → ★素材★
     → build → QA 三件套 → 自評分 → ★節拍表 + 關鍵格★ → ★草稿★ → ★正式版★ → 入庫
（★ = 用戶確認關卡）
```

本 skill 係說明書；效果庫（資料）放喺使用者電腦：`~/Documents/GitHub/video-fx-skill/`（下稱 LIBRARY，已同 GitHub 同步）。
效果目錄網頁（視覺效果（可按風格預設篩選）、聲效、調色、教學包參考頁四個分頁）：https://claude.ai/artifact/S4J778bzGTX56umuae9ZAQ

## 核心原則
1. **一定先問需求（硬性關卡）**：被召喚或收到素材後，第一件事係問三輪問題（第 1 節）。未問完、未確認需求摘要之前，唔好轉錄、唔好分析、唔好出分鏡。
2. **導演先行，逐關確認**：未經使用者確認，唔好揀效果、唔好渲染、唔好生成素材。五個關卡，每關用 AskUserQuestion 問「確認／要改」：
   0. Treatment + 動態系統卡：一頁導演表（見 `workflow/director.md`）+ 動態系統卡（主角元素、≤5 零件、tokens、入場／出場文法、聲效語言，見 `workflow/motion-system.md`；品牌已有卡就沿用）
   1. 分鏡：文字 + 效果庫預覽圖，唔渲染、唔生成
   2. 素材：列出要生成嘅素材、來源同額度，確認先生成
   3. 節拍表 + 關鍵格靜圖：build 完、QA 過咗之後出（`workflow/stills-gate.md`），用戶批咗先 render
   4. 草稿：`--quality draft` 渲染一次，只睇一張細 contact sheet
   5. 正式版：`--quality high` 渲染 + 換原音軌 + 核對
   詳見 LIBRARY `workflow/storyboard.md`。

**硬性規則（每條片都要遵守，詳見 `lessons/layout-safety.md`）**
- **一條片一套動態系統（最重要）**：所有畫面元素都由系統卡嘅零件生出嚟；效果庫效果已經 token 化（色、時長、緩動讀 CSS 變數），composition `<head>` 貼預設 `tokens.css` 再貼品牌 `brands/<brand>/tokens.css` 就自動換皮；揀效果按 registry 嘅 `component`（零件類別）同 `entry`（入場文法）對系統卡，`style_bound` 效果只限對應風格。新效果入庫跟 `workflow/add-effect.md`「零件同 tokens」一節。變化嚟自內容、狀態、構圖、節奏，唔係嚟自新效果。主角元素相隔 < 1 秒就變形過去，≥ 1 秒就退場再入。`node scripts/qa-motion.cjs index.html <motion-system.json>` 唔過唔准渲染。
- **一條片一個風格預設**：treatment 揀 `presets/SP-###`（字體、色彩意思、緩動、轉場、字幕、調色、聲效家族、效果白名單一套過）；composition `<head>` 貼該預設 `tokens.css`（品牌檔顏色之後覆蓋）。效果只喺白名單揀，白名單以外要寫理由。出草稿前 `node scripts/check-style.mjs index.html presets/SP-xxx` 要過：字體 ≤ 2、色相 ≤ 4、緩動 ≤ 4、轉場 ≤ 2、字幕一款。
- **先剪停頓同口頭禪**：轉錄後用 `tools/cut.py`（見 `lessons/cutting-cantonese.md`）出 clean.mp4；之後所有步驟用 clean.mp4 同 clean-transcript.json。醫療限定詞（唔、可能、建議、除非…）永遠唔自動剪。
- **冇背景音樂**：用戶上 IG 先加；只做聲效 + 輕度人聲清理。
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
4. 字幕款式同聲效：FX-039 光暈字幕或 FX-051 方框字幕；聲效密度少／中／多（由 sounds/ 聲效庫揀）。唔做背景音樂（用戶上 IG 先加）

**第三輪：素材同限制**
1. AI 生成素材：唔用／少量（例如 ≤ 20 credits）／可以放手用，出分鏡時報價
2. 講者出鏡：全程見到講者／可以用全屏過場蓋住講者
3. 剪停頓同口頭禪：按節奏剪（建議）／只剪呃嗯同頭尾／唔剪
4. 觀眾要記住乜 + 特別要求或禁忌：自由填寫（例如「膝痛唔一定要換骹」；唔要某顏色、要 logo、醫生名同職銜）。Hook 一定有（treatment 出三個選項），唔做結尾 CTA

**問完**：輸出「需求摘要」表（項目｜答案），入面一定有「風格預設」（按情緒：專業醫療 → SP-001、溫暖生活 → SP-002、活潑年輕 → SP-003、高級編輯感 → SP-004、新聞資訊 → SP-005）同「調色」兩行：寫推薦預設（例如「GR-001 專業專訪（按醫療健康推薦）」）；使用者喺特別要求講過顏色就跟佢。問一次「確認需求？」先進入第 2 節。

## 2. 分析（輕量）
- 有參考片：跟 `workflow/reference-to-style.md`：`scripts/analyze-ref.sh`（每 0.5 秒一格）→ `tools/ref_style.py`（鏡頭長度、色板、顆粒自動量度）→ 睇 sheet 填 `refs/<slug>/style-guide.md`（主角元素、字點入點出、轉場、質感…）→ 轉成動態系統卡 → shot list。**只拎文法，唔拎內容**（logo、角色、相片、原句、音樂唔抄）。YouTube 片唔好自己下載，請用戶俾檔。
- **參考片係英文（或非中文）**：每個有文字嘅手法按 `lessons/cjk-adaptation.md` 清單檢查，analysis.md 每段加「中文適應：good／adjust／poor + 要改咩」。用中文實際內容試渲染一格，縮到 360px 闊睇得清先算數。
- 揀效果：由 registry.json 按 `video_types`、`pace`（跟問卷答案）再按 `fits`、`mood` 篩選；排除 banned 同 REMOVED；`cjk_fit: poor` 預設唔推薦，優先 good。覆蓋規則：1 款基本字幕 + 1 個開場手法 + 1 × camera；15 秒以上加 1 × cutaway 或 list-chart；有列舉內容用 list-chart。檢查 `pairs_with`／`conflicts_with`。見 `workflow/recommend.md`。
- 調色分析：`python3 tools/grade.py analyze source.mp4` → 曝光、白色位偏色、膚色；有問題（偏暗、偏黃、膚色唔自然）喺分鏡講一句。
- 剪停頓同口頭禪（轉錄之後即做）：`python3 tools/cut.py analyze source.mp4 work/asr.json work --pace <fast|medium|slow>` → 睇 `work/review.md`，review 項目逐個決定（有疑問就問使用者，連同 treatment 一齊問）→ `python3 tools/cut.py apply source.mp4 work/cuts.json work/clean.mp4`（每接位 25ms 淡入淡出 + 輕度人聲清理；唔要清理加 `--no-voice`）。`edl.json` 嘅 `joins` 每個接位分鏡時要轉機位或者 FX-040。
- 轉錄：`tools/asr.py`（faster-whisper large-v3-turbo，language=yue，word timestamps）；低把握度字多數係口語位，要標示俾使用者核對。亂碼或重複段用 `condition_on_previous_text=False` 分段重轉。

## 2.5 關卡零：Treatment（導演表）
按 `workflow/director.md` 出一頁表：核心一句、觀眾問題、三個 hook 選項（A/B/C）、結構（hook → 2–4 body beat → payoff，寫 clean.mp4 時間）、視覺比喻、色彩意思（≤ 3 色）、風格預設、字幕、調色、聲效密度、剪輯節奏、講者佔比。問「確認 treatment？揀邊個 hook？」，**停低等答覆**，未確認唔好出分鏡。

## 3. 關卡一：分鏡
0. 出分鏡前逐個剔 `workflow/director.md` 嘅部門清單（故事節奏、字幕、動態、素材、調色一致性、聲效、QA）。
1. 每鏡加 `beat`（hook／setup／tension／proof／turn／payoff），效果強度跟 beat；超過 2.2 秒冇新視覺資訊寫 `holdReason`。效果只喺風格預設白名單揀。按句切鏡頭（每鏡長度跟節奏答案），寫 `storyboards/<project>.json`（格式見 `storyboards/_example.json`）：每鏡時間、講緊咩、畫面描述、FX-id、**字幕模式（基本字幕／由特效字取代，並寫出特效字）**、素材（source：canva／footage／higgsfield／stock／code）、生成描述、額度；要聲效就加 `sfx`（`[{"sfx":"SFX-001","t":3.8}]`，按效果嘅配搭聲效揀），分鏡網頁可以試聽。
2. `node scripts/build-storyboard.mjs storyboards/<project>.json` → html；stage 去雲端，用 Artifact 發佈（同一專案重用同一連結）。JSON 頂層加 `"grade": "GR-001"`；另外出調色對比圖 `python3 tools/grade.py compare source.mp4 storyboards/<project>-grade.jpg <推薦> <備選1> <備選2>`，同分鏡一齊俾使用者確認。
3. 確認問題逐項列出：效果庫以外嘅元素、`cjk_fit: adjust` 效果要改嘅參數、講者出現比例、每個效果用咗幾次、有冇類別缺可用效果。
4. 問使用者確認；要改就只改 JSON 再 build，唔好重寫。

## 4. 關卡二：素材
- 按 `workflow/assets.md` 次序：**Canva → 原片截圖 → Higgsfield → 有授權圖庫 → 代碼插圖**。
- Canva connector（`mcp__Canva__*`，用 ToolSearch 載入）：generate-image（9:16 用 PORTRAIT_9_16）、用戶已有素材。
- Higgsfield connector（`mcp__Higgsfield__*`）：每個專案 `create_project` 一次；生成前一律 `get_cost:true`，列總數確認先生成；多個素材用 batch + jobs_wait。詳見 `workflow/assets-higgsfield.md`。
- 代碼做得到嘅（UI、圖表、線條、字幕、圖示輪廓）唔好用 AI 生成；但效果 `needs` 要相片嘅，唔好用代碼插圖頂替而唔講。生成插圖唔使醫生審核。

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
- **QA 三件套（唔過唔准出節拍表／渲染）**：
  1. `python3 tools/qa.py check index.html chars.json`（字對聲、字幕逐字、字數、重疊、immediateRender）
  2. `node scripts/qa-stills.cjs <proj> frames qa_out`（安全區、logo、置中、字見到、結束後冇殘留、**畫面冇唔應該出現嘅字**）
  3. `node scripts/qa-motion.cjs index.html brands/<brand>/motion-system.json`（緩動、時長、入場、顏色、零件跟系統卡）
  manifest 每項要有 `comp`（零件）、`state`、`enter`、`beat`。
- **自評分**：按 `workflow/critique.md` 7 個維度評分寫 `critique.json`，`python3 tools/qa.py critique critique.json` 全部 ≥ 7 先交；最多自己改 3 輪。
- **節拍表 + 關鍵格**：`node scripts/keyframes.cjs` + `python3 tools/beatgrid.py` → Artifact 發佈，問用戶確認先 render（`workflow/stills-gate.md`）。
- **舊一致性檢查**：`node scripts/check-style.mjs index.html presets/SP-xxx` 冇 ✗。
- **渲染前清單**：逐項剔 `lessons/preflight-checklist.md` 15 項（時間軸墊底、video 唔放入有時間嘅 div、字幕硬收、冇 Math.random 等），再行 `hyperframes lint --json` 同 `validate`。
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
