---
id: FX-023
name: 飛舞元素群
name_en: flying-element-swarm
category: accent
family: [SP-002]
tags: [particles, butterflies, motion-path, decorative]
mood: [poetic, playful, editorial]
fits: [podcast-clip, lifestyle, education]
video_types: [動畫解說, 口播知識]
pace: [中]
pairs_with: [FX-026, FX-025, FX-024]
conflicts_with: []
needs: [cutout-asset]
brand_color_ready: true
source: ref3-instinct-interview 0:02–0:06
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
difficulty: medium
cjk_notes: ""
component: accent
entry: [cut]
---

## 效果
一群去背小物件（ref 用蝴蝶）由畫面一邊飛過，沿住唔同弧線、帶輕微旋轉同拍翼，喺米白紙質背景上襯托大字（believe your *instinct*）。

## 幾時用

抽象概念需要「生命感」；做兩段之間嘅轉場。

## 參數同節奏


- 6–10 隻，大小 40–90px，時間錯開 0.05–0.15s
- 每隻用 motionPath 或 x/y 分段 tween，1.5–2.5s，ease sine.inOut；rotation ±20°
- 拍翼：scaleX 1 ↔ 0.3，重複（有限次數）


## 實作重點

唔可以用 Math.random，用 seeded PRNG 生成路徑；repeat 要計準次數（唔好 -1）。

## 已知限制

需要去背素材（PNG／SVG）。
