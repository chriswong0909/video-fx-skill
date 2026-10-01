---
id: FX-020
name: 散落詞字幕
name_en: scattered-word-caption
category: text-fx
family: [SP-002, SP-004]
tags: [word-by-word, layout, mixed-type, b-roll]
mood: [cinematic, calm, editorial]
fits: [lifestyle, podcast-clip, education]
video_types: [紀錄 Vlog, 口播知識]
pace: [中, 慢]
pairs_with: [FX-030, FX-018]
conflicts_with: []
needs: [word-timestamps, face-box]
brand_color_ready: true
source: ref2-fitness-bloodsugar 0:10–0:12
learned: 2026-09-29
used_in: []
status: active
cjk_fit: adjust
cjk_notes: "中文冇空格，要先按意群分詞；散落後閱讀次序易亂，只用喺 8 個字以內嘅短句。"
placement: free
difficulty: medium
component: headline
entry: [rise]
---

## 效果
一句話嘅詞語唔排成一行，而係散落喺畫面唔同位置逐個出現（細字 + 一個斜體襯線重點詞），好似句子喺畫面入面「生長」。常疊喺 B-roll 上。

## 幾時用

情緒句、金句；B-roll 有大片空位。

## 參數同節奏


- 細詞 72px Sans 500；重點詞 150px Serif Italic
- 每詞 opacity + y 10，0.2s；位置預先排好（左上 → 中 → 右下）


## 實作重點

每個詞手動定位（absolute），避開畫面主體。
