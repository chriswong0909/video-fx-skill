# HyperFrames 渲染技術坑（實戰記錄）

## 必守
1. **全屏圖層（cutaway、gallery、畫廊等）要做成 clip**：`class="clip" data-start data-duration data-track-index`。
   只用 `opacity:0/1` 切換，喺軟件渲染（Linux ARM / SwiftShader）會出現大片黑色方塊殘影。（2026-09-28, doctor2-ref1style）
2. **唔好對 `<video>` 本身加 CSS filter / transform 動畫**，要包一層 wrapper（`#cam > #camInner > video`）再對 wrapper 做。
3. **z-index**：`#cam` 有 z-index 時，所有疊喺上面嘅絕對定位元素都要有更高 z-index，否則被遮（例如浮動問號）。
4. 同一元素同一屬性唔好兩條 tween 時間重疊（lint 會警告）。
5. 字幕 block 硬切換用 `tl.set(el,{opacity:1},start)` / `tl.set(el,{opacity:0},end)`；字幕元素細，冇黑塊問題。
6. 中文字體：用 Google Fonts CSS API 加 `&text=` 只下載用到嘅字（每個字重約 15–20KB），放 `assets/fonts/` 用 @font-face。
7. 出片後換返原音軌：`ffmpeg -i render.mp4 -i source.mp4 -map 0:v:0 -map 1:a:0 -c copy out.mp4`，再用 `ffmpeg -map 0:a -f md5 -` 對比。

## 環境（Cowork 本機 VM，Linux ARM64）
- `npx hyperframes browser ensure` 喺 Linux ARM64 會失敗；改用 `npx playwright install chromium`，再下載 `libxdamage1` deb（ports.ubuntu.com）解壓到 `~/xlibs`：
  `export LD_LIBRARY_PATH=~/xlibs/usr/lib/aarch64-linux-gnu`
  `export HYPERFRAMES_BROWSER_PATH=<chrome-headless-shell 路徑>`
- 使用者 kit 入面 node_modules 係 macOS 版，VM 要另外喺 scratch 做一份 Linux 版 `npm ci`。
- device_bash 每次最多 180 秒，而且背景 process 會隨指令結束被殺：長工作要拆段（例如逐 290 幀處理）。
- 渲染：`--workers 3 --no-low-memory-mode`，19 秒 1080×1920 draft 約 45 秒，high 約 65–100 秒。
- 已連接資料夾入面 `git` 會因為 lock 檔唔可以刪而失敗；喺 scratch 做好再 rsync 入去。

## 雲端 ↔ 本機傳大檔（2026-09-30）
- `device_commit_files` 每個檔 ≤ 20MB、每次 ≤ 100MB：大片用 `split -b 19m` 分段傳，本機 `cat` 返。
- **分段包含 mp4 檔頭（ftyp）嗰段會被改壞**（md5 唔同）：先 `gzip` 再傳，本機 `gunzip`；傳完一定核對 md5。
- 用同一個 stagedPath 重傳可能攞到舊內容：每次用新檔名。
- 雲端裝唔到 `hyperframes`（npm 403）同 `faster-whisper`（pip 冇）：ASR 同渲染都要喺本機做；本機 turbo 模型 80 秒音頻約 32 秒轉完。

## 疊喺影片上面嘅全屏圖層（2026-09-30）
- 暗角、紅閃呢類全屏圖層要做 clip（data-start／data-duration），而且 **z-index 要 ≥ 5**：z-index 3 喺 HyperFrames 渲染時會消失（瀏覽器預覽見到，出片唔見），改做 5 就正常。
- `#cam` 上面用 CSS filter（saturate／brightness）渲染時冇效果：要變暗用半透明圖層代替。
- 本機 VM 空間：80 秒片 draft 截圖要約 3GB 暫存；唔夠會 ENOSPC。可刪 `~/wl3`（冇用嘅 large-v3 模型）同 `~/tmp`。

## visibility 會繼承（2026-09-30，doctor2 v3 出事）
- HyperFrames 收 clip 係用 `visibility:hidden`。clip 入面嘅子元素如果自己 `tl.set(...,{visibility:'visible'})`，母層收咗佢都仲會見到（卡片內容、交叉線殘留喺之後成條片）。
- 規則：**頂層元素**用 visibility 控制出現；**clip 入面或者受 show() 控制元素入面嘅子元素**，一律用 opacity（或 display）控制。
- 入場動畫唔好用 `immediateRender:false`：開始前元素會見到，之後彈走再入（「可以慢跑」出咗又退再出）。用 fromTo 預設。
- 瀏覽器預覽模擬 clip 要用 visibility（唔好用 display:none），否則會遮住呢類 bug。
- 劃線動畫唔好用 SVG dasharray + non-scaling-stroke（會斷開、提早出現）；用 div bar + scaleX。

## 同一個元素重用（主角元素）要清返狀態（2026-09-30）
- 主角元素（#hero）入面每個字組用 `tl.set(opacity:1)` 開；**窗口完結要 `tl.set(opacity:0)` 收返**，否則下次 hero 再出現，舊字組仍然係 1，會疊埋一齊（doctor2 v5 靜圖發現）。
- `qa-stills.cjs` 已加「畫面有唔應該出現嘅字」檢查：每張截圖列出所有見到嘅字（計埋母層 opacity），唔屬於嗰刻 manifest 嘅就 ✗。

## 效果 token 化（2026-10-01）
- 效果顏色用 `var(--c-x, #後備)`／`color-mix()`；SVG 屬性入面 var() 唔生效，要寫喺 style。
- snippet 要有 tokens 讀取器（`window.EASE`／`window.DUR`）先用得 `DUR.*`；冇讀取器會 `DUR is not defined`，成段動畫唔出。
- `scripts/fx-shot.cjs` 可以一次過截晒 79 個效果，token 化前後逐張比對（平均像素差 > 3 就要人手睇）。

## 風格包卡掛入主檔（2026-10-01，doctor2 風格包版）
- **host 要有 z-index**：主檔講者包喺 `#cam{z-index:2}`，卡 host 冇 z-index 就會畫喺講者後面（全屏卡變透明、細卡完全唔見）。host 加 `class="cardhost"`：`.cardhost{position:absolute;inset:0;z-index:12}`，全屏卡 `.cardhost.t1{z-index:14}`。
- **host 都要帶 `data-dur` / `data-cues`**：卡用 `document.querySelector('[data-composition-id=X]')` 搵 ROOT，主檔入面會先搵到 host，冇呢兩個屬性就會用預設時間（逐項出現同唔到聲）。`cards.py use` 印出嘅 snippet 已經自動加。
- **舊主檔 CSS 會污染卡**：沿用舊 index.html 時，要刪走 `.card`、`.row`、`.side` 之類通用 class 規則，否則會套落卡入面同名 class。

## 長片要分段 render（2026-10-02，doctor2 風格包版）
- 本機 shell 每次最多 180 秒，而且背景程序會跟住收（nohup 都冇用）；80 秒片一次過 render 要 4 分鐘以上，會中途斷。雲端容器裝唔到 hyperframes（npm 403）。workers 8 會爆記憶體（4 核 4GB，用 4）。
- 做法：`python3 chunk.py T0 T1 名`（範本喺 `~/hf/d2k/chunk.py`）切一段獨立專案：所有 `data-start` 減 T0、講者 video 加 `data-media-start`、主時間軸用 `W.add(tl.tweenFromTo(T0,T1,{ease:'none'}),0)` 包住。**切位要揀冇卡嘅時間**（卡跨過切位會報錯）。
- 速度約 3.5–4 秒 render 1 秒片（draft）；每段 ≤ 28 秒先穩陣。之後 `ffmpeg -f concat -c copy` 駁返，再 mux 聲效混音。接駁位抽格對比過冇跳。

## 圖片要寫死闊同高（2026-10-02，黎青龍護肝篇草稿）
- 分段 render 最尾一段（5 秒短段），右上 logo 喺 4 個 worker 入面 3 個畫成又高又窄（`<img>` 只寫 width，高度靠圖片載入後自動計；worker 截圖時圖未解碼完）。
- 規則：主檔所有 `<img>`（logo、名牌框）CSS 一定寫 width **同** height。
- 檢查：render 完用 ffmpeg 逐格 crop logo 位，數品牌藍像素（`crop=278:132:742:228`），同中位數差 > 15% 嘅格就係出事；抽格 contact sheet 要包括每段頭尾。

## 雲端而家砌到專案同截圖（2026-10-03，40S）
- 雲端容器 `npx hyperframes`（0.8.114）裝到，預裝 Chromium 可以直接 `lint`／`snapshot`；`pip install faster-whisper` 都得（turbo 模型，39 秒音頻約 1 分鐘；用 `wave` 讀 16k wav 傳 numpy，唔好傳檔名，PyAV 版本唔夾）。上面「雲端裝唔到」嘅記錄已過時。
- 技能庫私有 repo 雲端 clone 唔到：用 `device_stage_files` 分批搬 tools、styles、brands、lessons（每批 ≤ 50 個檔）。
- 字型：lint 唔接受冇 @font-face 嘅系統字名（例如 Noto Sans CJK TC）；用 Google Fonts `&text=` 子集落 `assets/fonts/`，品牌 tokens 入面寫 @font-face（路徑 `assets/fonts/…`）。
- 卡入面嘅根元素 id 唔好用嚟加 class（掛入主檔後搵唔到）：用 `ROOT.querySelector('.rows')` 呢類內部元素。
- 主檔 manifest：每個 slot 要對返自己嘅 cue 時間，唔好全部用第一個 cue（qa.py 會報「早過講出嚟」）。

## 雲端工作區會被重置（2026-10-15，骨質疏鬆篇）
- 剪到一半雲端容器被回收，專案檔（index 模板、beats、caps、MG 腳本、剪接 plan）全部冇咗，要靠對話記錄逐步重建，嘢咗一個鐘。
- 規則：每出一版草稿，就將專案腳本（唔包大片）tar 一份 commit 返用戶電腦 `work/`；重建步驟寫喺 `workflow/examples/osteo/README.md`。
