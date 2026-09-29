---
id: FX-050
name: 同心圓脈衝標示
name_en: pulse-ring-indicator
category: accent
family: [SP-001]
tags: [indicator, pulse, pain-point, medical]
mood: [clinical, educational, urgent]
fits: [medical, public-health, education]
video_types: [醫療健康, 動畫解說]
pace: [中]
pairs_with: [FX-044, FX-036]
conflicts_with: []
needs: []
brand_color_ready: true
source: ref8-ha-heart-care 0:06.8–0:08.3
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: 原片係中文（廣東話旁白），字體同排版可直接沿用。
difficulty: easy
---

## 效果
喺插圖身體某個位置（例如胸口）出現紅橙色同心圓，一圈圈向外擴散，標示痛楚或者問題位置。

## 參數同節奏
- 3 個圓環，stroke 8px，顏色 #e8452c → #f5a623；中心實心點 14px
- 每圈 scale 0.3 → 1.4、opacity 1 → 0，0.9s，錯開 0.3s，重複次數按停留時間計（唔好用 repeat -1）

## 實作重點
位置用百分比對準插圖；同 FX-044 圓形格一齊用效果最好。
