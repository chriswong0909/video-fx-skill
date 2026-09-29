---
id: FX-036
name: 膠囊遮罩 + 標註線
name_en: capsule-mask-callout
category: layout
tags: [mask, capsule, callout, medical]
mood: [clinical, clean, educational]
fits: [medical, education, product]
video_types: [醫療健康]
pace: [中]
pairs_with: [FX-021, FX-037, FX-016, FX-050]
conflicts_with: []
needs: [cutout-or-photo]
brand_color_ready: true
source: ref7-spine-surgeon 0:03.5–0:05.5
learned: 2026-09-29
used_in: [doctor-stairs-breath]
status: active
cjk_fit: adjust
cjk_notes: 標籤最少 64px。
placement: layout
difficulty: easy
---

## 效果
相片／片段放入一個直身膠囊形（超大圓角）遮罩，擺喺深藍背景上；由相中某一點（患處）畫出一條幼白線去到一個細標籤（implant），下面再出大字 + 膠囊關鍵詞。

## 幾時用

指出身體部位、產品零件；醫療解說。

## 參數同節奏


- 膠囊：border-radius 999px，寬 360 高 600，白色 6px 邊
- 標註線：1.5–2px 白，弧形，dashoffset 0.4s；標籤白底深藍字 64px
- 膠囊入場 scale .9 → 1 0.35s；再畫線


## 實作重點

可以同 FX-037 膠囊關鍵詞一齊用，保持同一套圓角語言。
