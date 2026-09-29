---
id: FX-022
name: 手繪圈註
name_en: hand-drawn-annotation
category: accent
family: [SP-002, SP-005]
tags: [doodle, scribble, circle, underline]
mood: [playful, editorial, human]
fits: [podcast-clip, interview, education]
video_types: [口播知識, 訪問對談]
pace: [中, 快]
pairs_with: [FX-030]
conflicts_with: []
needs: []
brand_color_ready: true
source: ref3-instinct-interview 0:00–0:02
learned: 2026-09-29
used_in: [doctor-stairs-breath]
status: active
cjk_fit: good
placement: on-text
difficulty: easy
cjk_notes: ""
---

## 效果
重點詞外面用手繪筆觸畫一個圈（或者底線、剔號），好似有人拎筆喺畫面上圈重點。

## 幾時用

問題句、數字、年齡等要人留意嘅細詞。

## 參數同節奏


- 白色 4–6px，線頭圓角，略為唔規則（兩圈唔完全重疊）
- stroke-dashoffset 0.35s power1.out，喺詞語出現後 0.1s 開始畫


## 實作重點

SVG path 預先畫好幾款（圈、底線、箭嘴），按字闊縮放。
