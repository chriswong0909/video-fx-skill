---
id: FX-047
name: 打交叉禁止
name_en: cross-out-mark
category: accent
family: [SP-001, SP-003, SP-005]
tags: [cross, prohibit, crayon, warning]
mood: [clear, educational, friendly]
fits: [medical, public-health, education]
video_types: [動畫解說, 醫療健康]
pace: [中]
pairs_with: [FX-046, FX-044]
conflicts_with: []
needs: []
brand_color_ready: true
source: ref8-ha-heart-care 0:24.8–0:26.6
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: 原片係中文（廣東話旁白），字體同排版可直接沿用。
difficulty: easy
component: accent
entry: [draw]
---

## 效果
一個壞習慣插圖（煙）出現後，兩筆粗蠟筆紅線快速交叉畫過，表示「唔好做／戒除」。

## 參數同節奏
- 兩條線 stroke 26px #b3202c，linecap round，蠟筆質感（SVG turbulence filter 或者略為唔規則嘅 path）
- 第一筆 0.2s，停 0.05s，第二筆 0.2s；畫完 scale 1.05 → 1 輕震

## 實作重點
可配合 FX-046：先滑入插圖，0.3s 後打交叉。
