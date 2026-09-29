---
id: FX-085
name: 斜切色塊問題清單
name_en: diagonal-question-panel
category: list-chart
family: [SP-003]
tags: [agenda, questions, diagonal, panel, list]
mood: [energetic, bold, educational]
fits: [interview, education, podcast-clip, medical]
video_types: [訪問對談, 口播知識, 醫療健康, 紀錄 Vlog]
pace: [中, 快]
pairs_with: [FX-082, FX-084, FX-083]
conflicts_with: [FX-067, FX-010]
needs: []
brand_color_ready: true
source: ref19-forensic-podcast 0:52–1:01
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: "每條問題 8–14 字，粗黑 16:9 約 30px、9:16 最少 64px；9:16 色塊改由下方斜切入、佔下半 45%。"
placement: layout
aspect: "16:9"
difficulty: medium
---

## 效果
開場預告今集問題時，一大塊斜切品牌色塊（黃色，印滿淡色大問號圖案）由右邊滑入蓋住畫面右半，講者留喺左邊；跟住一條條白色標籤（前面有黃色圓形問號）逐條彈出：法醫工作時在做什麼？要如何透過遺體判斷死因？……

## 幾時用
片頭 agenda、今集問答大綱、醫生答問環節（「今集會答三條問題」）。

## 幾時唔好用
講者喺畫面右邊（會被遮）；問題多過 4 條。

## 參數同節奏
- 色塊：品牌色 #ffcf2e，clip-path polygon(22% 0,100% 0,100% 100%,0 100%)，x 100%→0 0.45s（power3.out）
- 底紋：大問號 SVG pattern，opacity .18，慢慢向上飄
- 標籤：白底 #fff、黑字 900、右下硬陰影 6px #111；問號圓 56px 品牌色 + 黑描邊
- 逐條：每條由右 x +40 + 淡入 0.25s（back.out），配講者講到嗰條先出

## 實作重點
色塊同標籤喺同一 group；講者唔使縮，只係右半被蓋。要做成 clip。

## 已知限制
左邊要有講者，構圖唔啱就改做全屏版本。
