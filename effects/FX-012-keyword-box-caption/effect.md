---
id: FX-012
name: 關鍵詞色塊字幕
name_en: keyword-box-caption
category: caption
tags: [kinetic-type, highlight-box, brand-color, word-sync]
mood: [clinical, clean, editorial]
fits: [medical, talking-head, corporate, education]
pairs_with: [FX-009, FX-010, FX-014]
conflicts_with: [FX-001]
needs: [word-timestamps]
brand_color_ready: true
source: original（doctor2-editorial，參考 ref1 carbs 標題）
learned: 2026-09-28
used_in: [doctor2-editorial]
difficulty: easy
---

## 效果
兩層字幕品牌版：細白字帶句，關鍵詞用品牌色實心色塊（bar，白字）或米白 chip（品牌色字）由左掃出，字逐隻升上；可加小黃色底線、警告三角、剔號。

## 幾時用
有品牌色要求嘅專業內容（醫療、企業）。

## 參數同節奏
- 細字 56px Sans 500；色塊字 120px Serif 900
- 色塊 scaleX 0 → 1（0.32s），比詞語早 0.05s；字 stagger 0.045s
- 裝飾：底線 0.42s 後掃出；三角／剔號 back.out 彈出

## 實作重點
顏色全部用 CSS 變數（--blue, --off, --yellow），換品牌只改變數。黃色只做細面積點綴。

## 已知限制
色塊太多會變廣告感，每句最多一個。
