---
id: FX-043
name: 道具附著入場
name_en: prop-attach-entrance
category: accent
family: [SP-002]
tags: [object, overlay, entrance, illustration]
mood: [friendly, playful, educational]
fits: [medical, education, explainer, product]
video_types: [動畫解說]
pace: [中]
pairs_with: [FX-042, FX-041]
conflicts_with: []
needs: [cutout-asset]
brand_color_ready: true
source: ref8-ha-heart-care 0:01.8–0:04.2
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: 原片係中文（廣東話旁白），字體同排版可直接沿用。
difficulty: easy
component: accent
entry: [scale, slide-edge]
---

## 效果
主角插圖出現後，一件相關道具（聽診器）由畫面邊滑入，好似「搭」落主角身上，同主角組成一幅完整圖，表示「檢查／照顧」呢個概念。

## 參數同節奏
- 道具去背 PNG，由右上方 x +300、rotation 15° 滑入，0.6s back.out(1.4)
- 落位後主角輕微 scale 1.03 → 1（被碰到嘅反應）0.2s

## 實作重點
道具同主角要同一插畫風格（同一批生成）。
