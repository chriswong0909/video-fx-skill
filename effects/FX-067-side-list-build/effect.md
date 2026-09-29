---
id: FX-067
name: 講者旁清單逐項出
name_en: side-list-build
category: list-chart
family: [SP-001, SP-002, SP-005]
tags: [list, side-panel, clean, minimal]
mood: [clean, journalistic, calm]
fits: [news, education, interview, medical]
video_types: [新聞資訊, 口播知識, 醫療健康]
pace: [慢, 中]
pairs_with: [FX-066, FX-064]
conflicts_with: [FX-038, FX-010]
needs: [list-content]
brand_color_ready: true
source: ref15-reporter-ivod 0:03–0:09
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: 每項 4–8 字，字 32–40px（畫面細可以加大）。
placement: layout
difficulty: easy
---

## 效果
講者坐喺畫面一邊（乾淨淺灰背景），另一邊由上而下逐項出現一列白色細長標籤（項目名 + 右邊細字），好似網站分類清單；講者全程喺畫面。

## 幾時用
介紹服務範圍、分類、清單（6–12 項），背景要有留白位。

## 參數同節奏
- 標籤：白底、1px 灰邊、圓角 6px、高 44px、闊 360px；字 30px Sans 700 深灰
- 每項 y 10 + opacity，0.12s，stagger 0.08s（清單長都唔會拖）
- 講者用 FX-040 平滑推鏡偏移去另一邊

## 實作重點
拍攝時要預留位置（講者坐偏）；或者用人像摳圖（見 lessons/relight.md）將講者移位。
