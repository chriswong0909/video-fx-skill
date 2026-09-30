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
