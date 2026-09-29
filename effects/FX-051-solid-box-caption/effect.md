---
id: FX-051
name: 實色方框字幕
name_en: solid-box-caption
category: caption
family: [SP-001, SP-005]
tags: [subtitle, box, broadcast, interview, brand-color]
mood: [clean, clinical, trustworthy, broadcast]
fits: [interview, talking-head, medical, podcast-clip, education]
video_types: [訪問對談, 醫療健康, 新聞資訊]
pace: [中, 慢]
pairs_with: [FX-017, FX-046]
conflicts_with: [FX-039]
needs: [word-timestamps]
brand_color_ready: true
source: 使用者提供截圖（醫聊室訪問片，上下分割雙人畫面）
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: 為中文設計：粗黑體白字，按意群 6–10 字一組、單行。
placement: lower
difficulty: easy
---

## 效果
白色粗黑體字放喺一個實色藍方框（#1063be）入面，直角、冇圓角、冇陰影，方框貼住文字闊度，置中擺喺畫面下方約 82% 高度。似電視新聞／訪問節目字幕，清楚、正式、有品牌感。

## 幾時用
訪問、對談、醫生講解；背景雜亂或者光暗變化大，需要字幕喺任何畫面都睇得清。

## 幾時唔好用
同 FX-039 基本字幕二揀一，全片只用一種基本字幕；想要輕盈、編輯感時（方框會較重）。

## 參數同節奏
- 方框底色 #1063be（品牌藍，可換 CSS 變數 --caption-box）；直角，padding 約 10px 26px
- 字：Noto Sans TC 900（或 700），約 80–84px，#fff，字距 2px，行高 1.2
- 位置：方框中心約 top 1580px（1920 高畫面），左右置中；一行最多 10–11 個字
- 斷句：按意群 6–10 字一組；每組硬切換，唔做動畫（或者 0.08s 淡入）
- 上下分割雙人畫面時放喺下半畫面講者胸口位置

## 實作重點
方框用 inline-block 包住文字（唔好全闊），`box-decoration-break: clone` 以防萬一斷行時每行都有方框。

## 已知限制
方框遮住畫面較多；兩行字會好厚重，盡量單行。
