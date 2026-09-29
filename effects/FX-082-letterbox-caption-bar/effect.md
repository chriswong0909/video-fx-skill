---
id: FX-082
name: 電影黑邊字幕
name_en: letterbox-caption-bar
category: layout
family: [SP-004]
tags: [letterbox, cinematic, caption-bar, ticker]
mood: [cinematic, premium, serious]
fits: [interview, documentary, podcast-clip]
video_types: [訪問對談, 紀錄 Vlog, 品牌企業, 新聞資訊]
pace: [慢, 中]
pairs_with: [FX-083, FX-084, FX-085]
conflicts_with: [FX-068]
needs: []
brand_color_ready: true
source: ref19-forensic-podcast 0:28–1:00
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: "字幕放喺下黑邊正中，白字粗黑 16:9 約 34px、9:16 最少 72px；上黑邊可放細字頻道名／贊助（52px 以上）。"
placement: layout
aspect: "16:9"
difficulty: easy
---

## 效果
畫面上下加一條實黑邊（似電影闊銀幕），字幕放入下面黑邊入面、唔再壓住畫面；上黑邊左角放頻道／節目名，右角放一行細黃字（贊助或者系列名）。畫面即刻有電影感，而字幕永遠唔會遮到人。

## 幾時用
訪問、紀錄、嚴肅題材；畫面資訊多、唔想字幕蓋住內容。

## 幾時唔好用
9:16 短片本身畫面已經窄（黑邊會再蝕位，只可以用細黑邊）；已經用 FX-068 頂部導航條。

## 參數同節奏
- 16:9：上下黑邊各 6%（約 65px）；9:16：上下各 9%（約 170px），字幕置下黑邊中
- 黑邊 #000 實色，入場時由 0 高度展開 0.4s（power2.out）
- 頂角細字 22px（16:9）；黃字 #ffcf2e

## 實作重點
黑邊係兩個固定 layer，z-index 最高；主畫面唔使縮，只係被遮。字幕 layer 改為相對黑邊置中。

## 已知限制
會遮住畫面上下 12–18%，構圖要預留。
