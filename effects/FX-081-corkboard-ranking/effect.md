---
id: FX-081
name: 水松板排行榜
name_en: corkboard-ranking
category: list-chart
family: [SP-005]
tags: [ranking, table, corkboard, highlight]
mood: [handmade, editorial, playful]
fits: [news, finance, education, commentary]
video_types: [新聞資訊, 口播知識, 動畫解說]
pace: [中, 慢]
pairs_with: [FX-078, FX-079, FX-074]
conflicts_with: []
needs: [ranking-data, photo-assets]
brand_color_ready: true
source: ref18-hk-retire-mgmtfee 1:06–1:13
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: "標題用手寫感粗圓體 2 行、每行 4–6 字；表格中文城市名 9:16 最少 52px，最多顯示 6 行。"
placement: layout
aspect: "16:9"
difficulty: medium
style_bound: true
bound_reason: "水松板木色係效果本身"
component: chart
entry: [rise, scale]
---

## 效果
水松板背景上釘住幾樣嘢：左上一張撕紙標題（2024年城市生活成本排名），右上一張相片（香港夜景），中間一張白紙排行榜表格；表格逐行出，然後螢光色條（黃、藍）逐條劃過要強調嘅排名，最後鏡頭慢推入表格。

## 幾時用
排名、榜單、比較表（生活成本排名、醫院輪候時間排名、各區發病率）。

## 幾時唔好用
超過 10 行嘅大表；需要精確數字對比（用 FX-072）。

## 參數同節奏
- 水松板：#b98a5a + 顆粒紋理；紙張陰影 0 8px 18px rgba(0,0,0,.35)，輕微旋轉 ±2°
- 表格：白紙 #fbfaf7，行高 44px（16:9）／64px（9:16），細灰分隔線
- 時序：標題紙 0.3s 拍落（scale 1.1→1）、相片 0.2s 後、表格行每行 0.08s 淡入
- 高亮：黃 #ffe34d、藍 #4fc3f7 色條 scaleX 0→1 0.35s，一條完先下一條
- 鏡頭：最後 2 秒 scale 1→1.12 推向高亮行

## 實作重點
表格用 HTML table 生成（數據寫 JSON），唔好用截圖（方便改）；撕紙標題可重用 FX-078 嘅 mask。

## 已知限制
數據要有來源；相片要有授權（Canva 圖庫或自己相）。
