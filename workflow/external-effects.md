# 外部效果配對（必做步驟；用戶 2026-10-15）

風格包（Kallaway／Vox）負責全片基礎設計（卡、字體、tokens）。**揀定風格包之後，一定要再睇外部效果來源**，替重點位揀 match 嘅效果，做成風格包嘅卡。
位置：Treatment 之後、節拍表之前（`skills/video-fx/SKILL.md` 第 5 節）。問卷第二輪「外部效果」選「今次唔使」先可以跳過（預設「照常配對」）。

## 1. 外部效果來源清單（之後會再加；加新來源喺呢度加一行，並寫明讀法）

| 來源 | 位置 | 讀法 |
|---|---|---|
| **text-motion-40**（40 款文字動畫） | 本機 `~/Documents/GitHub/text-motion-40/`；GitHub `chriswong0909/text-motion-40` | 先讀 `README.md` 使用規則，再用 `EFFECTS.md`（人睇）或 `effects.json`（程式讀）揀款；分格圖 `strips/`、單款短片 `clips/`、預覽網頁 `site/index.html`（換色即場睇）。**動作參數取自 `code/` 原作程式碼，場景自己按品牌設計**（見第 3 節）；`fonts/`、`PROMPT_TEMPLATE.md` 只作參考。本機搵唔到就用 GitHub MCP 讀 `chriswong0909/text-motion-40`。查詢：`python3 tools/ext_effects.py list --use 數字`／`show 29` |

## 2. 配對流程
1. **列重點位**：由 Treatment 結構列出 hook、標題（章節）、關鍵詞、數字、轉場，每位寫原句同大約時間。
2. **按作用揀**：每個位去來源搵作用 match 嘅效果（text-motion-40 用 EFFECTS.md 嘅「用於」欄；例如數字 → 29 Odometer、公告／決定 → 03 Text Stamp、強調 → 38 Highlight Text），**每個位最多 2 個候選**。
3. **一定先開分格圖**：揀之前打開 `strips/<編號>_<名>.jpg`（8 格，每 0.75 秒一格，一次完整動作），需要時睇 `clips/` 短片。**EFFECTS.md 標 ⚠ 嘅款（01、02、17、18、20、33）冇睇分格圖唔准用**——只睇提示詞字體、比例、節奏會走樣。需要時開 `site/index.html` 即場睇、換色。
4. **一條片外部效果以 2 至 3 款為主**，唔好太雜；同一作用用同一款（觀眾會認得）。
5. **出配對表俾用戶批**：欄位＝重點位｜原句｜候選效果（編號＋名）｜點解 match｜**場景設計**｜分格圖。寫 `matches.json`（格式見 `tools/ext_effects.py` 開頭），`python3 tools/ext_effects.py table matches.json out.html` 出頁（分格圖內嵌），用 Artifact 發佈，每輪改完用同一連結更新。**批咗先入節拍表。**
6. **全部唔適合**：可以一款都唔用，但配對表照出（列睇過邊啲、點解唔用），並喺 Treatment「外部效果」欄寫明。唔好硬用。

## 3. 做卡：動作取自原作，場景自己設計（2026-10-16 改；用戶批；唔好照搬原作畫面）

### 3.1 原則
一個效果＝**動作層**＋**場景層**。
- **動作層取自原作**：時間、緩動、先後次序（stagger）、結構。睇 `code/編號_名稱.js`（`python3 tools/ext_effects.py show 編號` 會列字體、字級、時長）。例：#29 逐位滾動、後一位慢 0.12 秒、`power3.out`；#32 切開 56/22px、0.45s `power3.out`；#37 11 點正弦波液面；#27 每字 0.1 秒。
- **場景層按品牌同內容自己設計**：背景、主體圖形、字點排、同講者關係。唔搬原作 487×160 橫幅、唔用原作深色底、唔用原作日文字體。
- 原因：2026-10-16 照搬 #29 原作 code 做出嚟，被用戶指明明顯差過骨質疏鬆篇手作嗰個場景（海軍藍橫幅、冇圖形、字細、字體唔係品牌）。骨質疏鬆篇做法（效果概念做靈感、場景自己畫）先係對嘅。
- 所以規則由「code 搬運、顏色只換 c」放寬為「**動作照原作，外觀跟品牌，可以自由設計**」。`cards.py adapt --ext`、`ext_effects.py fontcheck／brandfont` 降級做**起點同檢查工具**，唔做正式卡嘅預設。

### 3.2 流程
1. **配對表加「場景設計」**：每個候選寫清楚呢位要畫咩場景（matches.json 嘅 `scene` 欄；`table` 會顯示）。唔係只寫「用 #29」。
2. 讀原作 code，抽動作參數，寫入卡頭註解（動作取自 #N、外觀點設計）。
3. 做場景（全屏淺色 Healthy Days 風格；顏色只讀品牌 tokens；效果字 ≥ 76px；唔用 `Math.random`；全屏卡字幕照出）。
4. **先出一張最能代表嘅定格畫面俾用戶批**，批咗先做全動畫。
5. 驗收（必做）：有同類、已批嘅正式片場景就**並排對比**（上排正式版、下排新卡，同一時間點）；冇就對 `strips/` 睇動作、對品牌規格睇外觀。唔准淨係對分格圖就話過關。
6. 批咗 `cards.py verify <id> --note … --source "text-motion-40#N（動作）"` 入庫。**呢條片過咗之後**，將用到嘅場景抽成庫卡（文字、數字全部做 slot），下次同作用位直接用。

### 3.3 庫卡規格
- 位置 `styles/<style>/cards-9x16/<style>.x.<作用>.<款>.html`，登記 `style.json`／`portrait.json`（`source` 寫 `text-motion-40#N（動作）`）。
- 全部文字、數字做 `data-slot`（隱藏 `<i class="sl">` 放預設值，空白嘅自動隱藏）；`data-cues` 控制各階段開始秒數；`data-dur` 結尾 0.25 秒淡出，timeline 以 `.set({}, {}, 7)` 收尾，`window.__timelines[id]` paused、可 seek。
- 顏色用 `var(--accent)`、`var(--head)`、`color-mix()`；字體用 `var(--font-display)`，`cards.py use` 會檢查專案 `sans900.woff2` 夠唔夠字。
- 效果字 ≥ 76px、IG 安全區、純文字場景唔貼人面。

### 3.4 技術注意（盲測學到）
- 複雜字（例如「鈣」）用 `-webkit-text-stroke` 做輪廓，內部筆畫會重疊變亂線：改用淺灰藍填色做底，液體／填色層疊上面。
- 逐位／逐字動作字級要按字數計（打字卡：第一行 ≤ 130px、第二行 ≤ 150px，按 848px 寬自動縮）；切開類（#32）字總寬 ≤ 740px，否則切開位移（±120px）時會走出卡外。
- 需要「每格重算」嘅動作（#37 波浪）：用 proxy 物件 tween＋`onUpdate`，唔好用 `setInterval`，咁截圖／render 先 seek 得。
- 換字內容（#32 迷思→事實）用兩層 opacity 交換，唔好用 `.call()`（seek 唔保證觸發）。

### 3.5 已入庫卡（Healthy Days，kallaway 淺色）
| 卡 | 動作來源 | 場景 | 驗證 |
|---|---|---|---|
| `kallaway.x.stat.odometer` | #29 Odometer | 比例數字＋人形＋膠囊（重構自骨質疏鬆篇 mg_quarter） | 並排對正式版 v3，用戶批 |
| `kallaway.x.contrast.split` | #32 Split Halves | 迷思／事實反差：白卡切開，縫中「其實」 | 盲測（冇參考），用戶批 |
| `kallaway.x.meter.liquid` | #37 Liquid Fill | 大字液體量表＋百分比＋膠囊 | 盲測，用戶批 |
| `kallaway.x.text.typewriter` | #27 Typewriter | 白卡兩行打字提問 | 盲測，用戶批 |

骨質疏鬆篇另有 #03 蓋印、#38 螢光筆嘅手作場景（`workflow/examples/osteo/build.py`），未抽成庫卡；下次用到先抽。

### 3.6 盲測紀錄（2026-10-16）
測試方法：只讀原作動作、唔睇任何舊成品，場景自設；每款出定格畫面俾用戶批。三款第一版自己睇圖揾到問題（#37 輪廓線亂、#27 字細、#32 切開走出卡外），修後用戶批「效果很好」。結論：呢套「動作取自原作＋場景自設＋先批定格」可以喺冇參考下做到合格；穩定性靠品牌規格、定格批核、並排驗收同庫卡累積，唔靠代碼搬運。截圖 `workflow/examples/ext29/`。

## 4. 其他規則
- **節拍表**：每拍加欄「外部效果」，寫用咗邊款（例如 `text-motion-40 #29 Odometer`）或「冇」；`beats.json` 對應欄位 `ext`。
- **用過嘅場景要沉澱**：片完咗，將批過嘅場景抽成庫卡（第 3.2 第 6 點），唔好每條片由零再做。
- **版權**：來源只供個人參考學習（text-motion-40 README），repo 保持私人，唔好再發佈原片或程式碼；片入面用嘅係自己 HTML／GSAP 嘅版本。字體係 OFL 授權。
