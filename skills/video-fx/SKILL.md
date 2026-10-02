---
name: "video-fx"
description: "用 HyperFrames 剪片、加動態字幕、圖片同動態圖像卡（醫生口播、知識短片、Healthy Days 等）時使用：先問三輪需求，剪停頓，用風格包（Kallaway／Vox）加生成圖片，節拍表逐拍真截圖連聲效批核先 render，QA 後入庫同步 GitHub。"
---

# video-fx：風格包剪片 skill

**核心改變（2026-10-01，2026-10-02 用 doctor2 實戰後補充）：** 一條片嘅視覺由**一個風格包**負責（新手包 `kallaway` 或 `vox-explainer`），
唔再由效果庫逐個效果揀。風格包 = 一套完整設計（DESIGN.md + tokens.css + 數百張卡），每張卡係獨立 composition，
文字放 `data-slot`，顏色字體緩動讀 tokens。品牌（例如 Healthy Days）只覆蓋顏色同加品牌固定元素（logo、名牌、字幕）。
舊效果庫（`effects/`）降級做**技巧參考**：查「某種效果點做」先睇，唔直接放入片。

LIBRARY＝`~/Documents/GitHub/video-fx-skill/`（同 GitHub 同步）。效果目錄網頁：https://claude.ai/artifact/S4J778bzGTX56umuae9ZAQ（「風格包卡（主力）」分頁＝兩套風格包全部卡，標住邊張已有 9:16 版）。

```
問卷 → 轉錄 + 剪停頓 → Treatment（揀風格包、hook、結構、畫面比例）→ 素材（生成圖：先試 2 張定風格）
     → 砌專案 → 節拍表（每拍真截圖＋聲效＋字幕出唔出）→ 用戶批／改（通常 2–3 輪）→ QA → 草稿 → 正式版 → 入庫
（Treatment、圖片風格、節拍表、草稿、正式版＝用戶確認關卡）
```

## 核心原則
1. **一定先問需求（硬性）**：收到素材第一件事係問三輪問題（第 1 節）。未確認需求摘要唔好轉錄、分析、出方案。測試片都要問。
2. **一條片一個風格包**：`styles/kallaway`（現代發光玻璃；Healthy Days 預設用**淺色版** `--brand healthy-days`）或 `styles/vox-explainer`（紙感雜誌、手繪圈註）。全片所有圖像卡都喺同一個風格包揀，唔混用、唔加效果庫效果。風格包規則讀 `styles/<style>/DESIGN.md`（唔好做嘅嘢要跟）。
3. **卡片用到先改 9:16**：`python3 tools/cards.py list --style kallaway --portrait` 睇已有直向版嘅卡。要用嘅卡未有直向版 → `cards.py adapt <id>` 複製做起點，再按 `workflow/style-packs.md` 改版面，出預覽俾用戶批，批咗 `cards.py verify <id>`。改好嘅卡永久入庫，下次直接用。
4. **少而長嘅卡（新手包 video-beats 原則）**：一個話題一張卡，卡跟住話題存在（唔係每句閃一張）；tier1 全屏卡係重點標點（全片 2–4 張），tier2 支援卡（關鍵詞、清單、名牌）保留講者。每張卡答到一條問題：觀眾要記住乜？邊個概念要結構？邊個數字值得強調？見 `workflow/beats.md`。
5. **字對聲**：卡入面逐項出現時間用 `data-cues`，由 chars.json 逐字時間計（相對卡開始秒數）；字幕同卡文字要係講過嘅字（醫療限定詞唔准刪）。
6. **畫面比例同圖片**（用戶 2026-10-02）：口播片預設大約 **40% 見人物、40% 全屏（圖片為主，資訊卡最多 2 張）、20% 人物加圖片**；問卷要確認。Kallaway 冇圖片卡，用三張自家卡：`kallaway.x.image.full`（全屏圖）、`kallaway.x.image.split`（上圖下人）、`kallaway.x.image.pip`（胸口位圖片框，框入面張圖固定唔郁）。清單卡可以每行配圓形縮圖（slot p1–p4）。圖片用 Canva `generate-image` 生成，提示詞跟品牌檔「圖片風格」；**先試 2 張俾用戶定風格，批咗先全批生成**；落圖要用戶同意（`workflow/assets.md` 嘅分層 → 匯出 → curl）。Canva 連接冇「圖變片」，唔好話做到。
7. **節拍表＝真截圖**：先砌好專案，再用 `npx hyperframes snapshot --at …` 逐拍截圖，出一頁（Artifact）：每拍有截圖、時間、原句、卡 id、卡上字、**聲效（幾秒、邊個聲、對住咩動作）**、**字幕出唔出**。唔好用文字描述代替，唔好等到草稿先出現聲效。範例腳本喺 `workflow/examples/doctor2-k/`（build.py、page.py、page_tpl.html、sheet.sh）。
8. **品牌固定元素**：`brands/<brand>.md`（Healthy Days：右上 logo 常駐、名牌樣板、字幕方框、title tag）照舊，疊喺風格包上面；品牌色經 `brands/<brand>/tokens-<style>.css` 覆蓋風格包 tokens。

**硬性規則**
- **先剪停頓同口頭禪**：`tools/cut.py`（`lessons/cutting-cantonese.md`），之後全部用 clean.mp4 + clean 轉錄。
- **冇背景音樂**：只做聲效 + 輕度人聲清理。
- **字幕只得一款**（FX-051 方框或 FX-039 光暈，品牌指定優先）；**效果字已經交代嗰句，字幕就唔出**（節拍表每拍寫 `skipcaps`）；資訊卡時段唔出字幕；字幕唔准似卡字。醫療限定詞（有機會、可能、可以）要留喺效果字入面。
- **IG 安全區**（1080×1920）：左右 52px、頂 212、底 1556 以外唔放字；圖像置中 540。
- **效果唔好貼人面**（用戶 2026-10-02）：頭頂位唔放關鍵詞／卡，只留 logo；疊喺講者嘅卡（關鍵詞、警號、劃線、圖片框）放胸口／字幕位（top ≥ 980；圖片框 top 900 配闊鏡 1.0）；名牌放右下角；開場線條唔好橫過頸。上圖下人：講者塊面要喺圖片同字幕之間。
- **效果字唔細過字幕**：所有效果字 ≥ 76px（字幕 76px），大字 110–120px；畫面空就用大字，唔好角落一條細字。
- **左上標題條只做段落標題／分題**（84px），內容字用圖片頂部白底大字（big）或者膠囊（tags）。
- **跳鏡喺句與句之間**（長句可以喺逗號位）：轉機位、全屏入場退場都對返句邊。**人物接人物唔好硬切放大**（似跳鏡），用約 0.7 秒平滑推／拉；由全屏畫面返嚟講者先可以直接切。
- **唔加未要求嘅元素**；素材唔好靜靜雞降級（`workflow/assets.md`，Canva 第一，生成圖唔使醫生審核）。
- **基本調色**每條片都做：`tools/grade.py recommend` → `grade.py apply clean.mp4 <GR-id> graded.mp4`，HyperFrames 用 graded.mp4（音軌用 clean.mp4），唔好再疊調色 filter。
- **HyperFrames 坑**（`lessons/hyperframes-rendering.md`）：掛載卡嘅 host 一定要有 `data-composition-id`、`data-dur`、`data-cues`（`cards.py use` 印出嘅 snippet 已有）同 z-index（`.cardhost{position:absolute;inset:0;z-index:12}`，全屏 `.t1` 14），否則卡會喺講者後面、逐項時間唔啱；沿用舊主檔要刪走 `.card`、`.row` 呢類通用 class 規則；卡入面資產路徑用根目錄相對（`assets/…`，唔好 `../`）；querySelector 唔好用 template literal；visibility 會繼承（子元素用 opacity）；全屏層 z ≥ 5；`tl.to({}, {duration:END}, 0)` 墊底；唔好 `immediateRender:false`。

## 0. 連接 LIBRARY（同問卷同步做）
1. get_device_info；未有 `~/Documents/GitHub/video-fx-skill` 就 device_request_folder_access。
2. 讀 `styles/README.md`、選用風格包嘅 `DESIGN.md`、`brands/*.md`、`lessons/*.md`（必讀）、`workflow/beats.md`、`workflow/style-packs.md`。
3. LIBRARY 攞唔到：用 Artifact `action: read` 讀效果目錄網頁（`<script id="fxdata">` 有效果、聲效、調色、風格包卡 JSON）。

## 1. 開工問卷（強制）
已講過嘅預選並寫明「你講咗 X，確認？」；只有用戶明確講「唔使問」先可以跳過。完整選項見 `workflow/intake.md`。
**第一輪：基本** — 參考片（有／冇）｜平台同長度（9:16 保持原長／可剪短／16:9）｜品牌（brands/ 現有品牌檔／我提供）｜字幕寫法（口語／書面／中英）
**第二輪：風格同節奏** — 影片類型｜**風格包**（Kallaway 現代發光／Vox 紙感解說；品牌有預設就預選）｜節奏（快／中／慢）｜字幕款式同聲效密度（冇 BGM）
**第三輪：素材同限制** — AI 生成素材（唔用／少量／放手用，報價）｜圖片風格（品牌檔已有就預選；冇就先試 2 張）｜畫面比例（預設 40% 人物／40% 全屏／20% 人物加圖片）｜剪停頓（按節奏／只剪呃嗯／唔剪）｜觀眾要記住乜 + 禁忌（醫生名同職銜等）
問完出需求摘要表（含風格包、品牌、調色），問「確認需求？」。

## 2. 轉錄、剪停頓、分析
- 轉錄 `tools/asr.py`（faster-whisper turbo，language=yue，逐字時間）→ 改字表出 chars.json（`tools/words-template.py`）；低把握度字標出俾用戶核對。
- 剪停頓 `tools/cut.py analyze → review → apply`（醫療限定詞永不自動剪；每接位要轉機位或推鏡）。
- 調色 `tools/grade.py analyze / recommend / compare`。
- 有參考片：`workflow/reference-to-style.md`（只拎文法）；參考片風格同兩個風格包都唔夾 → 同用戶講，考慮按新手包 GUIDE 開新風格包（`styles/GUIDE-kit.md` build loop）。

## 3. 關卡：Treatment
一頁表（`workflow/director.md`）：核心一句、觀眾問題、三個 hook 選項、結構（hook → 2–4 段 → payoff，寫 clean.mp4 時間）、**風格包**、品牌、字幕、調色、聲效密度、剪輯節奏、**畫面比例**、圖片清單（每張對應邊句）。停低等確認。

## 4. 關卡：節拍表
按 `workflow/beats.md` 寫 `storyboards/<project>-beats.json`：每拍＝錨點原句、開始 t0／長度 dur、mode（person／full／card／split／pip）、卡 id、slots、cues、`skipcaps`（要收起嘅字幕開始秒數）、`sfx`（落地秒數、聲效、原因）。
- 先按句子邊界分段，逐段決定 mode，計出人物／全屏／人物加圖片各佔幾多秒，對返目標比例。
- 揀卡：`python3 tools/cards.py list --style <style> --portrait`（已驗證嘅 9:16 卡優先）；未有直向版先 `adapt`。
- 砌專案（第 6 節 1–3）→ lint → 逐拍截圖 → 出節拍表頁（Artifact 發佈，之後每輪改完用同一連結更新）→ 問確認。用戶意見改完要再截圖自己睇過先交。

## 5. 新卡預覽（併入節拍表）
- 節拍表用到但未有 9:16 版嘅卡：`cards.py adapt <id>`，按 `workflow/style-packs.md` 改（安全區、字級、data-cues、品牌色、出場動畫），用 `npx hyperframes snapshot` 出關鍵格／短 render 俾用戶睇。批咗 `cards.py verify <id> --note "…"`。
- 已驗證嘅卡唔使再批，除非 slot 內容長過上限。

## 6. Build + QA + 渲染
1. 專案放 `~/hf/<project>/`（assets：clean/graded mp4、gsap、logo、字型）。
2. 每張卡：`python3 tools/cards.py use <id> --project DIR --name beatNN --dur 秒 --slots '{…}' --cues 0.4,1.3 --brand healthy-days` → 將印出嘅 snippet 貼入 index.html（填 START、TRACK）。
3. index.html：講者 video（非計時 wrapper 做推鏡）、卡（data-composition-src）、品牌固定元素（logo、名牌、字幕）、manifest（`fx-manifest`：每個畫面字 = 卡 slot 文字 + 出現時間，俾 qa.py 對聲）。
4. QA：`npx hyperframes lint`（0 error）→ `python3 tools/qa.py check index.html chars.json`（字對聲、字數、重疊）→ `npx hyperframes snapshot --at …` 逐張卡關鍵格睇（安全區、遮面、字清唔清）→ `workflow/critique.md` 自評分（`qa.py critique`，全部 ≥ 7）。
5. 聲效：`sfx-events.json`（卡元素落地格）→ `tools/sfx_plan.py` → `tools/sfx.py mix`（`lessons/sound-mixing.md`）。
6. 草稿 `npx hyperframes render --quality draft`（本機 VM：`source ~/hf/env.sh`，`--workers 4 --no-low-memory-mode`）。**本機每次最多 180 秒、背景程序唔會留低、雲端裝唔到 hyperframes**：長過約 25 秒嘅片用 `python3 tools/hf_chunk.py T0 T1 名 專案資料夾` 切段（切位揀冇卡嘅時間），逐段 render（每段一個 call），`ffmpeg -f concat -c copy` 駁返。抽格 contact sheet（包括接駁位前後）自己先睇 → 俾用戶。聲效我聽唔到，要同用戶講明。正式版 `--quality high`；冇聲效：`ffmpeg -i render.mp4 -i clean.mp4 -map 0:v:0 -map 1:a:0 -c copy out.mp4`（md5 核對音軌）；有聲效：`tools/sfx.py mix clean.mp4 cues.json mix.m4a` 再 mux（原聲音量不變 + limiter）。核對長度、幀數、比例。成品放素材旁 `output/`。

## 7. 入庫（每次剪完）
1. 用戶批咗草稿先 `cards.py verify` 新卡；`styles/<style>/portrait.json` 記低用過邊條片、slot 上限。
2. 新技術坑寫 `lessons/`；品牌改動寫 `brands/`；聲效／調色 `used_in` 更新。
3. 用戶否定某張卡：講「唔啱用」→ `portrait.json` 該卡加 `"banned": "原因"`，之後唔再揀；只係某條片唔啱 → 唔好禁。舊效果庫刪除規則照 `effects/REMOVED.md`（編號永不重用）。
4. `node scripts/build-registry.mjs && node scripts/build-gallery.mjs`，重新發佈效果目錄（同一連結）。
5. Git：本機 `git add -A && git commit`（確認冇 `.git/*.lock` 殘留）；只改文字檔可以用 GitHub MCP push_files 推上 `chriswong0909/video-fx-skill` main（推完用 get_file_contents 對 sha）；有二進制檔就提醒用戶雙擊 `推上GitHub.command`，之後 list_commits 核對。永遠唔好問 token／密碼。
6. 最後同用戶講：新改／驗證咗邊幾張卡（卡 id）、lessons 加咗乜、GitHub 推咗未。

## 模式
| 模式 | 用喺 | 檔 |
|---|---|---|
| A 真人口播（預設） | 醫生片、講者片 | `modes/talking-head.md` |
| B B-roll 插片 | 已剪好嘅片按字插動態卡 | `modes/broll.md` |
| C 無真人講解 | 旁白 + 全動態／生成鏡頭 | `modes/explainer.md` |
| D 產品／品牌宣傳 | 網址、UI 截圖做宣傳 | `modes/promo.md` |

## 原則
- 同用戶講廣東話，簡潔，新手友善；用到嘅卡註明卡 id。
- 未睇過實際畫面唔好話「適合」；推薦之前先出預覽。工具做唔到嘅嘢（例如 Canva 圖變片）要查清楚先答，唔好估。
- 用戶每次指出嘅通用問題（位置、字級、跳鏡、聲效）要寫入 `brands/` 或 `lessons/`，下條片唔好再犯。
- 唔作假帳號、假數據、假認證；示意圖標明「示意」；生成素材前講明額度。