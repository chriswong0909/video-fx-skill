---
id: FX-072
name: 圖案柱狀圖生長
name_en: pattern-bar-chart
category: list-chart
family: [SP-004]
tags: [bar-chart, data, flags, comparison]
mood: [editorial, dramatic, premium]
fits: [finance, education, news, explainer]
video_types: [口播知識, 新聞資訊, 動畫解說]
pace: [中, 快]
pairs_with: [FX-066, FX-074, FX-053]
conflicts_with: [FX-034]
needs: [data-source]
brand_color_ready: true
source: ref17-hk-retire-north 0:03–0:10
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: "標題 serif 中文 16:9 約 44px、9:16 最少 72px；數值標籤用數字 + 單位，唔好長句。"
placement: center
aspect: "16:9"
difficulty: medium
---

## 效果
深藍灰紋理底上，一排直條由基線向上逐條生長，每條直條入面填住圖案（國旗、醫院 logo、藥物顏色等），最高嗰條旁邊彈出紅色數值標籤（HK$8,600,000）加小箭嘴；頂部一行淡灰 serif 標題。比普通柱狀圖有記憶點。

## 幾時用
比較幾個地方／組別嘅數字（各地平均退休儲蓄、各國中風率、各年齡組病例數）。

## 幾時唔好用
數據超過 8 組；數字差距太細（生長動畫睇唔出分別）；冇可靠數據來源。

## 參數同節奏
- 底 #1a2130 + 裂紋紋理 opacity .35；基線 2px #c9b98a
- 直條闊 64px（16:9）／90px（9:16），間距 18px，圖案 background-size cover
- 生長：scaleY 0→1（transform-origin bottom），每條間隔 0.12s，0.6s power3.out；由右至左或由低至高
- 數值標籤：最後一條長完 0.2s 後，紅色 serif 字 + 斜箭嘴畫出 0.3s

## 實作重點
高度按真實數據比例計（寫喺 snippet data 陣列）；國旗等圖案用 SVG 或圖片，唔好用 emoji。數據來源寫入字幕或註腳。

## 已知限制
唔好造假數據；圖案太花會搶數字，最多一種圖案系列。
