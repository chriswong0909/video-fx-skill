---
id: FX-062
name: 物件跌落堆疊
name_en: object-drop-physics
category: accent
family: [SP-003]
tags: [physics, drop, bounce, stacking]
mood: [playful, energetic]
fits: [education, product, explainer, entertainment]
video_types: [動畫解說, 產品廣告]
pace: [快, 中]
pairs_with: [FX-061, FX-063]
conflicts_with: []
needs: [cutout-asset]
brand_color_ready: true
source: ref13-mingjai-ketchup 0:05–0:08、0:48–0:50
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: 同文字無關。
placement: layout
difficulty: medium
---

## 效果
一堆去背物件由畫面頂跌落，落入容器（購物車、碗）或者疊成金字塔，有落地回彈同輕微旋轉，表示「好多」「塞滿」「爆量」。

## 參數同節奏
- 每件：y -1200 → 目標，0.45s ease bounce.out 或 power2.in + 0.1s 回彈；rotation ±15°（seeded）
- stagger 0.06–0.1s；總長 1–1.5 秒
- 可加輕微 motion blur（blur 4px → 0）

## 實作重點
位置預先計好（seeded PRNG），唔好用 Math.random；物件多時用細圖。
