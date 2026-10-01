---
id: FX-041
name: 皺紙紋背景
name_en: paper-texture-backdrop
category: cutaway
family: [SP-002]
tags: [background, paper, texture, handmade]
mood: [warm, friendly, educational]
fits: [medical, education, public-health, explainer]
video_types: [動畫解說, 醫療健康]
pace: [中, 慢]
pairs_with: [FX-042, FX-044, FX-048]
conflicts_with: [FX-031]
needs: []
brand_color_ready: true
source: ref8-ha-heart-care 0:05.6–0:07.4
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: 原片係中文（廣東話旁白），字體同排版可直接沿用。
difficulty: easy
style_bound: true
bound_reason: "皺紙紋背景嘅紙色同粒子係效果本身"
component: cutaway
entry: []
---

## 效果
全片用米白皺紙做底：淡淡摺痕格紋 + 紅藍小墨點（似印刷飛墨），所有插圖同文字都放喺上面，有手作、親切嘅教育海報感。

## 幾時用
冇講者嘅純動畫解說、公共衛生教育、醫療科普；想要溫暖親切而唔係冷冰冰科技感。

## 參數同節奏
- 底色 #efe9df；摺痕：兩組 linear-gradient 格線（間距約 1/4 畫面），opacity .06–.1
- 墨點：40–80 粒 2–6px 圓點，紅 #c8323c／藍 #2d5aa8，opacity .5–.8，seeded PRNG 固定位置
- 背景全片靜止（唔好郁，否則會搶插圖）

## 實作重點
用一張預先生成嘅紙紋 PNG 最靚（可以 Higgsfield 生成 seamless paper texture），或者純 CSS + SVG 圓點。
