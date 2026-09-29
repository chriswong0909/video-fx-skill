---
id: FX-026
name: 單字閃卡
name_en: one-word-flash-card
category: transition
tags: [flash, solid-bg, one-word, rhythm]
mood: [bold, minimal, dramatic]
fits: [podcast-clip, interview, motivational]
video_types: [口播知識, 訪問對談]
pace: [快]
pairs_with: [FX-023, FX-018]
conflicts_with: []
needs: []
brand_color_ready: true
source: ref3-instinct-interview 0:06.5–0:07.8
learned: 2026-09-29
used_in: [doctor-stairs-breath]
status: active
cjk_fit: adjust
cjk_notes: 英文細階單字 → 中文每張 2–3 個字，字級最少 200px。
difficulty: easy
---

## 效果
全屏純色卡（先白底黑字，再深紅底白字），中間只得一個粗無襯線字（always → instinct.），每張 0.4–0.7 秒硬切，好似重拍打喺節奏上。

## 幾時用

金句嘅最後一兩個字、段落轉折，配合語氣重音。

## 參數同節奏


- 字 120px Sans 800，字距 -1px，句號保留增加肯定感
- 色：淺底 #efefef／深紅 #6e1d1d（跟 ref）或者品牌主色
- 冇入場動畫（硬切先有力），最多加 0.1s scale 1.05 → 1


## 實作重點

每張卡做 clip（data-start/duration），唔好用 opacity 切全屏層。
