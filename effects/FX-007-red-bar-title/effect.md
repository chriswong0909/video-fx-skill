---
id: FX-007
name: 紅條標題
name_en: red-bar-title
category: caption
tags: [title, highlight-bar, top]
mood: [warm, editorial]
fits: [talking-head, podcast-clip, education]
pairs_with: [FX-009, FX-001]
conflicts_with: []
needs: []
brand_color_ready: true
source: ref1-glucose-podcast 13:4–15:0（carbs）
learned: 2026-09-28
used_in: [doctor2-ref1style]
difficulty: easy
---

## 效果
畫面頂部一個大標題，字嘅下半部有一條紅色色塊由左掃出，字本身米白斜體帶深紅陰影；下面再跟一行細字。

## 幾時用
新話題／關鍵名詞開始時，放喺講者頭頂空位。

## 參數同節奏
- 字 140px Serif 900，color #fff4e8，text-shadow 0 3px 0 #8e241f，skew -10°
- 色塊 #b8352c，高 62px，bottom 22px；scaleX 0 → 1 0.35s，字 stagger 0.05s 升上

## 實作重點
講者要推近兼向下移（camInner y +200 左右）空出頭頂位置。

## 已知限制
淺色背景上要改用深色字。
