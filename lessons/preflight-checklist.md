# 渲染前檢查清單（preflight）

每次 `npx hyperframes render` 之前逐項剔。任何一項唔過 → 先改，唔好「試下 render 睇下」。
工具：`npx hyperframes lint --json` → `npx hyperframes validate` → `node scripts/preflight.mjs`（如有）→ `render --strict`。

## A. 時間軸
1. 每個 clip 都有 `data-start` / `data-duration` / `data-track-index`，而且數值由分鏡表 T（秒）計出嚟，唔好人手估。
2. 時間軸墊底：`tl.to({}, {duration: TOTAL}, 0)`，TOTAL = 成條片長度，避免結尾黑一格。
3. 同一 track 上嘅 clip 唔重疊；同一元素嘅兩個 tween 唔重疊（例如 FX-040 推入要喺下一個推入前 0.12s 完）。
4. 冇 `repeat: -1`；要循環就計好次數。

## B. 影片元素
5. `<video>` 一定 `muted playsinline`；聲音由獨立 `<audio>` 或混音檔處理。
6. `<video>` 唔可以放喺有 `data-start` 嘅 div 入面；要包就用冇時間屬性嘅 wrapper，時間屬性寫喺 video 本身。
7. 唔好對 `<video>` 直接做動畫（scale / x / opacity），郁佢個 wrapper。
8. `<video>` 唔加 `class="clip"`；同一原片第二個畫面（PIP、打格）用 `data-media-start` 對返原片時間。

## C. 字幕同文字
9. 字幕放 body 層，track ≥ 20，z-index 高過所有效果層。
10. 每句字幕結束用 `visibility:hidden` 硬收（唔好只靠 opacity 0），避免殘影。
11. 唔好用 `translateX(-50%)` 置中字幕；用 left:0 right:0 + text-align:center，或者 inline-block 行。
12. 字幕闊度要量：CJK 每字約 1em、英文約 0.55em；超過安全區就縮字（最細 72px）或者斷行。
13. 安全區：x 90–930、y 200–1600（9:16, 1080×1920）；IG 底部 UI 範圍唔放重要字。

## D. 確定性
14. 冇 `Math.random()`／`Date.now()`；要隨機用 seeded mulberry32。
15. 封面同最後一格要檢查：render 完抽 poster（0.0s）同 lastframe（TOTAL−0.04s）睇有冇黑格、殘字、未完成動畫。

## 已知限制
- FX-080 面部打格：要第二條同一原片 `<video>`（`data-media-start` 同主片對齊）+ face-box 關鍵點；HyperFrames 冇內建人臉追蹤，要先用工具出 face-box。醫生專業內容唔用。
- 16:9 效果（effect.md `aspect: "16:9"`）用喺 9:16 片前要重新排版，唔好直接縮細。
