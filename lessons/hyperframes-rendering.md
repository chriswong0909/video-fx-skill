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
