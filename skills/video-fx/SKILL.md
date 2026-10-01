---
name: "video-fx"
description: "用 HyperFrames 剪片、加動態字幕同動態圖像卡（醫生口播、知識短片、Healthy Days 等）時使用：必定先問三輪需求，剪停頓同口頭禪，用風格包（新手包 Kallaway／Vox 解說，9:16 用到先改）做全片視覺，寫節拍表（講稿原句做錨點、一個話題一張卡），卡片預覽批核先 render，做 QA 同自評分，剪完入庫並同步 GitHub。"
---

# video-fx：風格包剪片 skill

**核心改變（2026-10-01）：** 一條片嘅視覺由**一個風格包**負責（新手包 `kallaway` 或 `vox-explainer`），
唔再由效果庫逐個效果揀。風格包 = 一套完整設計（DESIGN.md + tokens.css + 數百張卡），每張卡係獨立 composition，
文字放 `data-slot`，顏色字體緩動讀 tokens。品牌（例如 Healthy Days）只覆蓋顏色同加品牌固定元素（logo、名牌、字幕）。
舊效果庫（`effects/`）降級做**技巧參考**：查「某種效果點做」先睇，唔直接放入片。

LIBRARY＝`~/Documents/GitHub/video-fx-skill/`（同 GitHub 同步）。效果目錄網頁：https://claude.ai/artifact/S4J778bzGTX56umuae9ZAQ（「教學包參考頁」分頁＝兩套風格包全部卡）。

```
問卷 → 轉錄 + 剪停頓 → Treatment（揀風格包、hook、結構）→ 節拍表（錨點＋卡＋slot）
     → 卡片 9:16 預覽批核（未改過嘅卡先改）→ build → QA → 自評分 → 草稿 → 正式版 → 入庫
（Treatment、節拍表、卡片預覽、草稿、正式版＝用戶確認關卡）
```

## 核心原則
1. **一定先問需求（硬性）**：收到素材第一件事係問三輪問題（第 1 節）。未確認需求摘要唔好轉錄、分析、出方案。測試片都要問。
2. **一條片一個風格包**：`styles/kallaway`（現代暗底發光玻璃，Healthy Days 預設）或 `styles/vox-explainer`（紙感雜誌、手繪圈註）。全片所有圖像卡都喺同一個風格包揀，唔混用、唔加效果庫效果。風格包規則讀 `styles/<style>/DESIGN.md`（唔好做嘅嘢要跟）。
3. **卡片用到先改 9:16**：`python3 tools/cards.py list --style kallaway --portrait` 睇已有直向版嘅卡。要用嘅卡未有直向版 → `cards.py adapt <id>` 複製做起點，再按 `workflow/style-packs.md` 改版面，出預覽俾用戶批，批咗 `cards.py verify <id>`。改好嘅卡永久入庫，下次直接用。
4. **少而長嘅卡（新手包 video-beats 原則）**：一個話題一張卡，卡跟住話題存在（唔係每句閃一張）；tier1 全屏卡係重點標點（全片 2–4 張），tier2 支援卡（關鍵詞、清單、名牌）保留講者。每張卡答到一條問題：觀眾要記住乜？邊個概念要結構？邊個數字值得強調？見 `workflow/beats.md`。
5. **字對聲**：卡入面逐項出現時間用 `data-cues`，由 chars.json 逐字時間計（相對卡開始秒數）；字幕同卡文字要係講過嘅字（醫療限定詞唔准刪）。
6. **品牌固定元素**：`brands/<brand>.md`（Healthy Days：右上 logo 常駐、名牌樣板、字幕方框、title tag）照舊，疊喺風格包上面；品牌色經 `brands/<brand>/tokens-<style>.css` 覆蓋風格包 tokens。

**硬性規則**
- **先剪停頓同口頭禪**：`tools/cut.py`（`lessons/cutting-cantonese.md`），之後全部用 clean.mp4 + clean 轉錄。
- **冇背景音樂**：只做聲效 + 輕度人聲清理。
- **字幕只得一款**（FX-051 方框或 FX-039 光暈，品牌指定優先），有卡大字顯示緊嗰句唔出字幕；字幕唔准似卡字。
- **IG 安全區**（1080×1920）：左右 52px、頂 212、底 1556 以外唔放字；圖像置中 540；唔遮面（講者頭位要預留）。
- **最細字**：卡標題 ≥ 96px、卡內文 ≥ 64px、字幕 76–80px、註腳 ≥ 44px。
- **唔加未要求嘅元素**；素材唔好靜靜雞降級（`workflow/assets.md`，Canva 第一，生成圖唔使醫生審核）。
- **基本調色**每條片都做（`tools/grade.py recommend`）。
- **HyperFrames 坑**（`lessons/hyperframes-rendering.md`）：掛載卡嘅 host 一定要有 `data-composition-id`；卡入面資產路徑用根目錄相對（`assets/…`，唔好 `../`）；querySelector 唔好用 template literal；visibility 會繼承（子元素用 opacity）；全屏層 z ≥ 5；`tl.to({}, {duration:END}, 0)` 墊底；唔好 `immediateRender:false`。

## 0. 連接 LIBRARY（同問卷同步做）
1. get_device_info；未有 `~/Documents/GitHub/video-fx-skill` 就 device_request_folder_access。
2. 讀 `styles/README.md`、選用風格包嘅 `DESIGN.md`、`brands/*.md`、`lessons/*.md`（必讀）、`workflow/beats.md`、`workflow/style-packs.md`。
3. LIBRARY 攞唔到：用 Artifact `action: read` 讀效果目錄網頁（`<script id="fxdata">` 有效果、聲效、調色、風格包卡 JSON）。

## 1. 開工問卷（強制）
已講過嘅預選並寫明「你講咗 X，確認？」；只有用戶明確講「唔使問」先可以跳過。完整選項見 `workflow/intake.md`。
**第一輪：基本** — 參考片（有／冇）｜平台同長度（9:16 保持原長／可剪短／16:9）｜品牌（brands/ 現有品牌檔／我提供）｜字幕寫法（口語／書面／中英）
**第二輪：風格同節奏** — 影片類型｜**風格包**（Kallaway 現代發光／Vox 紙感解說；品牌有預設就預選）｜節奏（快／中／慢）｜字幕款式同聲效密度（冇 BGM）
**第三輪：素材同限制** — AI 生成素材（唔用／少量／放手用，報價）｜講者出鏡（全程見到／可以用全屏卡蓋住）｜剪停頓（按節奏／只剪呃嗯／唔剪）｜觀眾要記住乜 + 禁忌（醫生名同職銜等）
問完出需求摘要表（含風格包、品牌、調色），問「確認需求？」。

## 2. 轉錄、剪停頓、分析
- 轉錄 `tools/asr.py`（faster-whisper turbo，language=yue，逐字時間）→ 改字表出 chars.json（`tools/words-template.py`）；低把握度字標出俾用戶核對。
- 剪停頓 `tools/cut.py analyze → review → apply`（醫療限定詞永不自動剪；每接位要轉機位或推鏡）。
- 調色 `tools/grade.py analyze / recommend / compare`。
- 有參考片：`workflow/reference-to-style.md`（只拎文法）；參考片風格同兩個風格包都唔夾 → 同用戶講，考慮按新手包 GUIDE 開新風格包（`styles/GUIDE-kit.md` build loop）。

## 3. 關卡：Treatment
一頁表（`workflow/director.md`）：核心一句、觀眾問題、三個 hook 選項、結構（hook → 2–4 段 → payoff，寫 clean.mp4 時間）、**風格包**、品牌、字幕、調色、聲效密度、剪輯節奏、講者佔比、全屏卡上限。停低等確認。

## 4. 關卡：節拍表
按 `workflow/beats.md` 寫 `storyboards/<project>-beats.json`：每拍＝錨點原句（chars.json 搵到）、開始／結束、tier、卡 id、slot 內容、cues、聲效。
- 揀卡：`python3 tools/cards.py list --style <style> --tier tier2 --purpose label`；優先揀已有 9:16 版（`--portrait`）。
- 用 `python3 tools/beatgrid.py` 出節拍表頁（Artifact 發佈），問確認。

## 5. 關卡：卡片預覽
- 節拍表用到但未有 9:16 版嘅卡：`cards.py adapt <id>`，按 `workflow/style-packs.md` 改（安全區、字級、data-cues、品牌色、出場動畫），用 `npx hyperframes snapshot` 出關鍵格／短 render 俾用戶睇。批咗 `cards.py verify <id> --note "…"`。
- 已驗證嘅卡唔使再批，除非 slot 內容長過上限。

## 6. Build + QA + 渲染
1. `npm`-free 專案：`~/hf/<project>/`（assets：clean/graded mp4、gsap、logo、字型）。
2. 每張卡：`python3 tools/cards.py use <id> --project DIR --name beatNN --dur 秒 --slots '{…}' --cues 0.4,1.3 --brand healthy-days` → 將印出嘅 snippet 貼入 index.html（填 START、TRACK）。
3. index.html：講者 video（非計時 wrapper 做推鏡）、卡（data-composition-src）、品牌固定元素（logo、名牌、字幕）、manifest（`fx-manifest`：每個畫面字 = 卡 slot 文字 + 出現時間，俾 qa.py 對聲）。
4. QA：`npx hyperframes lint`（0 error）→ `python3 tools/qa.py check index.html chars.json`（字對聲、字數、重疊）→ `npx hyperframes snapshot --at …` 逐張卡關鍵格睇（安全區、遮面、字清唔清）→ `workflow/critique.md` 自評分（`qa.py critique`，全部 ≥ 7）。
5. 聲效：`sfx-events.json`（卡元素落地格）→ `tools/sfx_plan.py` → `tools/sfx.py mix`（`lessons/sound-mixing.md`）。
6. 草稿 `npx hyperframes render --quality draft`（本機 VM：`source ~/hf/env.sh`，`--workers 4 --no-low-memory-mode`；device_bash 每次 ≤ 180 秒）→ 抽格 contact sheet 自己先睇 → 俾用戶。正式版 `--quality high` + 換原音軌 + 核對長度幀數。成品放素材旁 `output/`。

## 7. 入庫（每次剪完）
1. 新改好嘅 9:16 卡：`cards.py verify`；`styles/<style>/portrait.json` 記低用過邊條片、slot 上限。
2. 新技術坑寫 `lessons/`；品牌改動寫 `brands/`；聲效／調色 `used_in` 更新。
3. `node scripts/build-registry.mjs && node scripts/build-gallery.mjs`，重新發佈效果目錄（同一連結）。
4. Git：本機 `git add -A && git commit`；只改文字檔可以用 GitHub MCP push_files 推上 `chriswong0909/video-fx-skill`（推完對 sha）；有二進制檔就提醒用戶雙擊 `推上GitHub.command`。永遠唔好問 token／密碼。

## 模式
| 模式 | 用喺 | 檔 |
|---|---|---|
| A 真人口播（預設） | 醫生片、講者片 | `modes/talking-head.md` |
| B B-roll 插片 | 已剪好嘅片按字插動態卡 | `modes/broll.md` |
| C 無真人講解 | 旁白 + 全動態／生成鏡頭 | `modes/explainer.md` |
| D 產品／品牌宣傳 | 網址、UI 截圖做宣傳 | `modes/promo.md` |

## 原則
- 同用戶講廣東話，簡潔，新手友善；用到嘅卡註明卡 id。
- 未睇過實際畫面唔好話「適合」；推薦之前先出預覽。
- 唔作假帳號、假數據、假認證；示意圖標明「示意」；生成素材前講明額度。
