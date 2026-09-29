---
id: FX-053
name: 全屏素材配直排大字
name_en: fullframe-stock-bigtext
category: cutaway
tags: [b-roll, stock, big-type, vertical-text]
mood: [bold, energetic, cinematic]
fits: [finance, education, talking-head]
video_types: [口播知識, 品牌企業]
pace: [快]
pairs_with: [FX-052, FX-054]
conflicts_with: []
needs: [broll]
brand_color_ready: true
source: ref9-fire-investment 0:04–0:09、0:20–0:30
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: 直排中文大字每行 1 個字，一次 2–4 個字最易讀。
placement: center
difficulty: easy
---

## 效果
講到抽象概念時切去全屏素材（錢罌、硬幣、股票圖、鈔票），上面疊超大白色／半透明直排中文字（每個 150–250px），字逐隻出現；素材本身慢推或者有物件移動（手寫粉筆字、硬幣加疊）。

## 幾時用
快節奏口播，每 3–5 句插一個 1–2 秒全屏素材，解悶兼強調概念。

## 參數同節奏
- 素材：真實相片或短片（stock／Higgsfield 生成），可加暗角
- 字：Noto Sans TC 900，白色 85% 不透明 或 黃色重點（#f5d21b）；直排用 writing-mode: vertical-rl
- 每字 0.1s stagger 淡入 + y 20
- 每段 1–2 秒

## 實作重點
全屏層做 clip；字同素材顏色對比要夠（淺底用深灰字）。
