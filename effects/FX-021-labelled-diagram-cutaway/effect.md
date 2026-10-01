---
id: FX-021
name: 標註圖解過場
name_en: labelled-diagram-cutaway
category: cutaway
family: [SP-001]
tags: [diagram, medical, callout, explainer]
mood: [clinical, educational]
fits: [medical, education, science]
video_types: [醫療健康, 動畫解說]
pace: [中]
pairs_with: [FX-017, FX-036]
conflicts_with: []
needs: [illustration-or-photo]
brand_color_ready: true
source: ref2-fitness-bloodsugar 0:08–0:10
learned: 2026-09-29
used_in: [doctor-stairs-breath]
status: active
cjk_fit: adjust
cjk_notes: "原標籤 24px 太細，最少 64px；每個標籤最多 6 個字。"
difficulty: medium
component: cutaway
entry: [rise, scale]
---

## 效果
淺色全屏底，中間一幅醫學插圖（例如正常 vs 高血糖血管切面並排），每部分有細標籤同指示線；頂部細字 + 大粗字標題，底部再出關鍵詞（Blood Sugar）。

## 幾時用

解釋身體機制、對比「正常 vs 異常」。

## 參數同節奏


- 背景 #ece8e3；插圖佔中間 50%
- 標籤 64px（最少），指示線 2px，逐條 0.1s stagger 畫出
- 標題：細字 → 大字（FX-017 同一套節奏）


## 實作重點

插圖用 SVG（可控制每部分動畫）或者去背 PNG；標註線用 stroke-dashoffset 畫出。

## 已知限制

醫學插圖要準確，最好由客戶提供或者審核。
