---
id: FX-042
name: 線稿變彩色
name_en: line-to-color-reveal
category: transition
family: [SP-002]
tags: [illustration, line-draw, reveal, crayon]
mood: [friendly, educational, warm]
fits: [medical, education, explainer]
video_types: [動畫解說, 醫療健康]
pace: [中]
pairs_with: [FX-041, FX-043, FX-048]
conflicts_with: []
needs: [illustration]
brand_color_ready: true
source: ref8-ha-heart-care 0:00.0–0:01.8
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: 原片係中文（廣東話旁白），字體同排版可直接沿用。
difficulty: medium
---

## 效果
主角插圖（心臟）先以彩色線稿一筆筆畫出，然後顏色由淡到實填滿，變成蠟筆質感彩圖。開場 1–1.5 秒內完成。

## 幾時用
開場主角登場、介紹器官或者產品。

## 參數同節奏
- 線稿：SVG path stroke-dashoffset 0.6s，紅藍兩色線
- 填色：彩色圖 opacity 0 → 1 + 由下至上 clip-path 揭開，0.5s，喺線稿畫到 70% 開始
- 最後線稿淡走 0.2s

## 實作重點
需要兩層素材：線稿（SVG 或透明 PNG）+ 彩色圖（同一構圖）。可以用 Higgsfield 生成彩圖，再用描邊工具轉線稿；或者只做「彩圖由白色溶入」簡化版。
