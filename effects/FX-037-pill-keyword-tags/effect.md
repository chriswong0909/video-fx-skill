---
id: FX-037
name: 膠囊關鍵詞 + 浮動小標籤
name_en: pill-keyword-tags
category: text-fx
family: [SP-001]
tags: [pill, tags, keyword, floating]
mood: [clean, modern, clinical]
fits: [medical, education, product, talking-head]
video_types: [醫療健康, 口播知識]
pace: [中, 快]
pairs_with: [FX-036, FX-038, FX-017]
conflicts_with: []
needs: [word-timestamps, face-box]
brand_color_ready: true
source: ref7-spine-surgeon 0:02–0:03、0:09.5–0:11、0:13–0:14.5
learned: 2026-09-29
used_in: [doctor-stairs-breath]
status: active
cjk_fit: adjust
cjk_notes: "英文大楷 → 中文用 Black；膠囊同浮動標籤最少 64px。"
placement: headroom
difficulty: easy
component: capsule
entry: [draw, rise]
---

## 效果
大粗字（remove、patients）旁邊有細字前導，重點補充詞放入膠囊形色塊（藍底白字 disc／淺灰底深藍字 game changer）；有時周圍再飛出幾個細膠囊標籤（younger、healthier）好似貼紙。

## 幾時用

醫療、產品解說，需要清楚標示關鍵名詞。

## 參數同節奏


- 大字 150px Sans 900 深藍 #1c3d6e（淺底）／白（深底）
- 膠囊：radius 999，padding 6px 22px，64px 字；scaleX 0 → 1 由左 0.25s
- 小標籤：64px，藍底白字，由大字位置彈出到四周 0.3s back.out


## 實作重點

所有圓角一致（999px）先有統一感。
