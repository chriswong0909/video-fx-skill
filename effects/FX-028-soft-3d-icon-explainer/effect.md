---
id: FX-028
name: 柔和 3D 圖示解說
name_en: soft-3d-icon-explainer
category: cutaway
family: [SP-001]
tags: [icons, 3d, explainer, sequence, clinical]
mood: [clean, clinical, calm, educational]
fits: [medical, education, science]
video_types: [醫療健康, 動畫解說]
pace: [中]
pairs_with: [FX-029, FX-025, FX-018, FX-046]
conflicts_with: [FX-015]
needs: [3d-icons]
brand_color_ready: true
source: ref4-brain-explainer 0:01–0:05
learned: 2026-09-29
used_in: [doctor-stairs-breath]
status: active
cjk_fit: adjust
cjk_notes: "標題最少 72px。"
difficulty: medium
---

## 效果
淡藍漸變背景（有淡淡嘅線條圖示做底紋），中間逐個出現柔和 3D 圖示（腦 → 眼 → 行路公仔），每個配一個細標題，逐個換，好似 app 教學動畫。

## 幾時用

解釋「幾樣元素」「幾個功能」；醫療、科普，想要乾淨專業感。

## 參數同節奏


- 背景 linear-gradient(#eaf5fb → #bcd7e8)，底紋線條圖示 opacity .25
- 圖示 220–300px，放圓形淺色底座上；標題 72px Sans 700 深藍灰
- 換圖：舊圖 scale→0.8+淡出 0.2s，新圖 scale 0.6→1 back.out 0.35s
- 每個約 1–1.5 秒


## 實作重點

圖示用 3D 風 PNG（可以 AI 生成，要去背）或者 Lottie；冇素材就用 emoji 以外嘅 SVG 圖示 + 柔和陰影。
