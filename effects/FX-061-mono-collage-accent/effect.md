---
id: FX-061
name: 黑白拼貼 + 單一亮色
name_en: mono-collage-accent
category: cutaway
tags: [collage, monochrome, cutout, accent-color, history]
mood: [quirky, editorial, bold]
fits: [education, history, explainer, entertainment]
video_types: [動畫解說, 口播知識]
pace: [中, 快]
pairs_with: [FX-059, FX-060, FX-062, FX-063]
conflicts_with: [FX-015]
needs: [cutout-asset]
brand_color_ready: true
source: ref12-mingjai-aprilfool 0:05–1:12、ref13-mingjai-ketchup 0:03–0:51
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: 同文字無關。
placement: layout
difficulty: hard
---

## 效果
全屏白底或黑底，用黑白去背相片（雕像、建築、人物、物件）砌成拼貼場景，只有「主角物件」用一隻鮮色（例：藍綠 #2ee6d6）上色，其他全部黑白；物件逐件彈入、放大、移位，講故事似翻繪本。

## 幾時用
歷史、冷知識、品牌故事解說；冇講者或者講者只喺頭尾出現。

## 參數同節奏
- 背景 #f4f4f4 或 #1a1a1a（段落之間黑白互換做節奏）
- 所有素材 grayscale(1) contrast(1.15)；主角物件用 duotone 或直接上亮色
- 每個畫面 2–3 秒，物件 scale 0.8 → 1、y 40 → 0 入場 0.3s；可疊半色調 (halftone) 紋理

## 實作重點
素材量大：預先整理去背 PNG；亮色全片只用一隻；可以用 Higgsfield 生成物件再去背。

## 已知限制
製作時間長，要大量去背素材。
