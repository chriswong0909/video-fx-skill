---
id: FX-048
name: 雙色章節標題
name_en: two-tone-section-title
category: text-fx
family: [SP-001, SP-002, SP-005]
tags: [title, section, two-tone, outline]
mood: [friendly, educational, clear]
fits: [medical, public-health, education, explainer]
video_types: [動畫解說, 醫療健康]
pace: [中]
pairs_with: [FX-041, FX-044, FX-046]
conflicts_with: []
needs: []
brand_color_ready: true
source: ref8-ha-heart-care 0:16.0–0:18.0
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: 原片係中文（廣東話旁白），字體同排版可直接沿用。
difficulty: easy
component: headline
entry: [rise]
---

## 效果
畫面頂部一個粗圓體章節標題，兩種顏色（深藍 + 粉紅，重點字用粉紅），厚白描邊，整段固定唔郁；換章節時舊標題快速淡走、新標題彈入。

## 幾時用
解說片分章節（引言／徵狀／預防）；配合內容格或者插圖輪播。

## 參數同節奏
- 字 88–100px 圓體粗字；主色 #1f4e9c、重點 #e2476f；-webkit-text-stroke 12px #fff（paint-order stroke）
- 位置 top 150–200px 置中
- 入場：y -30 + opacity，0.3s back.out；換章節時舊標題 0.15s 淡走

## 實作重點
圓體中文字可用 Google Fonts「M PLUS Rounded 1c」做英數，中文用粗黑體 + 大描邊模擬圓體感。
