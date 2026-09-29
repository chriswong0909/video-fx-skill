---
id: FX-063
name: 放射光束背光
name_en: radial-light-burst
category: accent
tags: [rays, burst, reveal, hero]
mood: [dramatic, playful, triumphant]
fits: [education, product, explainer, entertainment]
video_types: [動畫解說, 產品廣告]
pace: [中, 快]
pairs_with: [FX-061, FX-062]
conflicts_with: []
needs: []
brand_color_ready: true
source: ref13-mingjai-ketchup 0:26–0:29
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: 同文字無關。
placement: layout
difficulty: easy
---

## 效果
主角物件（例：神秘配方、產品）出現時，後面放射出一束束亮色光（8–12 條三角形光束），慢慢旋轉，營造「重大發現」「隆重登場」感覺。

## 參數同節奏
- 光束：conic-gradient 做（亮色同透明交替），顏色跟單一亮色（#2ee6d6）opacity .6
- 入場 scale 0 → 1、opacity 0 → .6，0.4s；之後 rotation 0 → 20° 慢轉
- 配合主角 scale 1.1 → 1 輕彈

## 實作重點
用 conic-gradient + radial mask 令光束中間實、外面淡。
