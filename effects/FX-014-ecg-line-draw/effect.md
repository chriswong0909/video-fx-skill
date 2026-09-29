---
id: FX-014
name: 心電圖線描繪
name_en: ecg-line-draw
category: accent
tags: [line-draw, svg, medical, heart]
mood: [clinical, medical]
fits: [medical]
video_types: [醫療健康]
pace: [中]
pairs_with: [FX-010, FX-021]
conflicts_with: []
needs: []
brand_color_ready: true
source: original（doctor2-editorial）
learned: 2026-09-28
used_in: [doctor2-editorial, doctor2-ref1style, doctor-stairs-breath]
status: active
cjk_fit: good
difficulty: easy
cjk_notes: ""
---

## 效果
一條心電圖線由左至右畫出（stroke-dashoffset），講到心臟相關詞語時做點綴；變奏：不規則心律版本。

## 幾時用

心臟、健康、監測相關內容。

## 參數同節奏

線寬 7px、品牌色、白色 drop-shadow 光暈；0.9s power1.inOut

## 實作重點

放喺字幕上方（唔好壓住字），用 `attr:{'stroke-dashoffset'}` tween。
