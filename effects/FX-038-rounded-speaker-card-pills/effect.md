---
id: FX-038
name: 圓角講者卡 + 膠囊清單
name_en: rounded-speaker-card-pills
category: layout
family: [SP-001]
tags: [pip, card, list, pills, 3d-object]
mood: [clinical, clean, modern]
fits: [medical, education, talking-head]
video_types: [醫療健康]
pace: [中]
pairs_with: [FX-037, FX-036]
conflicts_with: [FX-010]
needs: [list-content]
brand_color_ready: true
source: ref7-spine-surgeon 0:05.5–0:09.5
learned: 2026-09-29
used_in: [doctor-stairs-breath]
status: active
cjk_fit: adjust
cjk_notes: "卡闊有限：卡內字最少 72px、每行最多 7 個字；膠囊最少 64px。"
placement: layout
difficulty: medium
---

## 效果
講者縮入深藍背景中間嘅圓角直身卡，粗白大楷字幕放喺卡入面（講者胸口位置），卡下面逐項彈出淺灰膠囊清單（Fusion Implant、Lumbar Disc Replacement），每項旁邊有一個 3D 黃色物件同時彈出。

## 幾時用

講者列舉選項／療程，想保留講者同時有清單。係 FX-010 嘅「深色、膠囊」版本。

## 參數同節奏


- 背景 #1c3d6e；卡 540×780 radius 26
- 字幕 72px Sans 900 白色大楷，卡內底部
- 膠囊 #e8ecf2 深藍字 64px，由左滑出 0.3s；3D 物件 scale 0 → 1 back.out 0.35s


## 實作重點

用 FX-010 同一套 #cam clipPath 縮放技術，改 inset 同 radius。
