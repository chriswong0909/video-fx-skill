---
id: FX-025
name: 虛線路徑連接
name_en: dashed-path-connector
category: accent
tags: [path, connector, line-draw, diagram]
mood: [editorial, playful, educational]
fits: [education, podcast-clip, explainer]
video_types: [動畫解說, 口播知識]
pace: [中]
pairs_with: [FX-024, FX-023, FX-028]
conflicts_with: []
needs: []
brand_color_ready: true
source: ref3-instinct-interview 0:04.5–0:06.5
learned: 2026-09-29
used_in: [doctor-stairs-breath]
status: active
cjk_fit: good
difficulty: easy
---

## 效果
一條彎曲虛線由一個元素畫向另一個元素（例如由電視畫向腦），終點元素隨即出現，表示「由 A 去到 B」嘅關係或者思考路徑。

## 參數同節奏


- 線 3px 深灰，dash 10 8，彎曲 C 曲線
- 用 mask 或者 dashoffset 由起點畫到終點 0.6–0.9s
- 終點物件 scale 0.6 → 1 back.out，喺線畫完前 0.1s 開始


## 實作重點

虛線本身用 stroke-dasharray，所以「畫出」要用 SVG mask 包住一條實線 mask path 做 dashoffset。
