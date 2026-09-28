---
id: FX-001
name: 兩層金色斜體字幕
name_en: two-tier-gold-caption
category: caption
tags: [kinetic-type, serif, gradient-text, word-sync]
mood: [warm, editorial, premium]
fits: [talking-head, podcast-clip, education, medical]
pairs_with: [FX-002, FX-009, FX-015]
conflicts_with: [FX-012]
needs: [word-timestamps]
brand_color_ready: true
source: ref1-glucose-podcast 0:00–0:10
learned: 2026-09-28
used_in: [doctor2-ref1style]
difficulty: easy
---

## 效果
上面一行細、幼身白色無襯線字逐詞出現；重點詞用超大粗襯線字，金橙漸變、斜體（skew -10°），逐字模糊放大入場。

## 幾時用
講者口播，每句有一個關鍵詞。暖色、生活、健康、知識類。

## 幾時唔好用
品牌要求冷色或者極簡；重點詞太長（>6 個中文字會太闊）。

## 參數同節奏
- 細字 58px Sans 300，白色 + 陰影；大字 150px Serif 900
- 漸變 #ffe08a → #f7a82a → #d9620b，drop-shadow
- 細字：y 24 → 0，blur 8 → 0，0.3s；大字每字 stagger 0.07s，scale 1.25 → 1，0.45s power3.out
- 一句講完即硬切下一組（唔做淡出）

## 實作重點
中文冇斜體，用 `transform: skewX(-10deg)` 模擬；漸變字用 `background-clip:text`，要逐字包 span 先可以逐字動。

## 已知限制
漸變字喺淺色背景對比度低，只適合疊喺人物／深色位置。
