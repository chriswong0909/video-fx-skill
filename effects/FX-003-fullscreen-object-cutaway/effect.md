---
id: FX-003
name: 全屏物件過場
name_en: fullscreen-object-cutaway
category: cutaway
tags: [b-roll, illustration, object, label]
mood: [warm, editorial]
fits: [talking-head, podcast-clip, education, medical]
pairs_with: [FX-001, FX-004, FX-015]
conflicts_with: []
needs: [illustration-or-photo]
brand_color_ready: true
source: ref1-glucose-podcast 3:00–4:00（腦）
learned: 2026-09-28
used_in: [doctor2-ref1style]
difficulty: medium
---

## 效果
講到某個名詞時，切去全屏純色／暖色背景，中間一個立體感物件（ref1 用腦部相片），上方細字 + 米色標籤框大字，物件緩慢旋轉；原聲繼續。

## 幾時用
講到具體器官、產品、概念，時長 1–2.5 秒。

## 幾時唔好用
講者表情係重點嘅句子；冇合適物件素材而插圖會太卡通時。

## 參數同節奏
- 背景 radial-gradient(#8a6452 → #3e271e)
- 標籤：#f3e6d3 底、Serif 900 130px、圓角 14、陰影；back.out 0.4s 彈入
- 物件 scale .75 → 1、y 60 → 0，0.6s；之後 2 秒內旋轉 -4°
- 可加「變化」：例如心臟出裂紋 + 降飽和度（表示衰退）

## 實作重點
**一定要用 clip（data-start/duration/track-index）**，唔好淨係用 opacity（見 lessons）。插圖用 SVG radial gradient + 高光 + 地面陰影做立體感。

## 已知限制
冇真實相片時，SVG 插圖質感較扁平，同 ref1 有差距；有素材應換相片。
