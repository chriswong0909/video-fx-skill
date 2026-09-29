---
id: FX-005
name: 橫向卡片畫廊
name_en: horizontal-card-gallery
category: list-chart
tags: [list, cards, scroll, gallery]
mood: [warm, editorial]
fits: [education, medical, product, podcast-clip]
video_types: [口播知識, 醫療健康, 產品廣告]
pace: [中]
pairs_with: [FX-006]
conflicts_with: [FX-010, FX-044]
needs: [list-content]
brand_color_ready: true
source: ref1-glucose-podcast 17:00–18:9（BREAD/PASTA/RICE）
learned: 2026-09-28
used_in: [doctor2-ref1style, doctor-stairs-breath]
status: active
cjk_fit: adjust
cjk_notes: "卡闊 600px，標題 100px 最多 5 個字；skew 對中文效果一般，可唔斜。"
difficulty: medium
---

## 效果
全屏淺色底，一排直身卡片（每張有圖 + 上方斜體標題）橫向滑過，講到邊項就停喺邊張。

## 幾時用

列舉 2–5 項（病徵、產品、步驟）。

## 幾時唔好用

項目多過 5 個；需要同時比較全部項目（改用 FX-010）。

## 參數同節奏


- 卡 600×820，圓角 26，間距 640；標題 Serif 900 104px #8e241f skew -10°
- track 入場 x +260 → 0（0.9s），之後每項 0.8s power2.inOut 移 -640
- 卡入場 y 80、rotation 3 → 0，比標題早 0.25s


## 實作重點

要做成 clip。每張卡內容可以係相片或 SVG 插圖；時間對準 ASR 詞語時間。

## 已知限制

冇相片時插圖較簡單。
