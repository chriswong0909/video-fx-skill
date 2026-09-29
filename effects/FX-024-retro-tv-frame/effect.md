---
id: FX-024
name: 復古電視框
name_en: retro-tv-frame
category: layout
family: [SP-005]
tags: [frame, retro, pip, tv, tint]
mood: [nostalgic, editorial, playful]
fits: [podcast-clip, interview, film]
video_types: [訪問對談, 口播知識]
pace: [中]
pairs_with: [FX-025, FX-023, FX-026]
conflicts_with: [FX-010]
needs: [tv-frame-asset]
brand_color_ready: true
source: ref3-instinct-interview 0:03.5–0:06
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
placement: layout
difficulty: medium
cjk_notes: ""
---

## 效果
講者片段放入一部舊式 CRT 電視機框入面（黑白或紅色單色調），電視放喺米白背景上，周圍有標籤字，可以配合虛線路徑移動。

## 幾時用

引用另一段片／另一個人講嘢；懷舊或者「回憶」感。

## 參數同節奏


- 電視框 PNG（去背）+ 內部 video 用 clip-path 對準屏幕位
- 屏幕：grayscale(1) contrast(1.1)，或者紅色 multiply 疊色
- 入場：scale 0.9 → 1 + 輕微 rotate 3°，0.4s back.out


## 實作重點

video 放 wrapper 入面，對 wrapper 做 filter（唔好直接對 video）。
