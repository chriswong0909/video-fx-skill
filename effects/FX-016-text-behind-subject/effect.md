---
id: FX-016
name: 文字喺人物後面
name_en: text-behind-subject
category: text-fx
family: [SP-004]
tags: [depth, matting, layering, big-type]
mood: [premium, editorial, dramatic]
fits: [talking-head, medical, fitness, product]
video_types: [口播知識, 醫療健康, 產品廣告]
pace: [快, 中]
pairs_with: [FX-017]
conflicts_with: []
needs: [matting, face-box]
brand_color_ready: true
source: ref7-spine-surgeon 0:00.5–0:01.5
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: "方塊字被頭遮住會難認：揀筆畫少嘅字，遮蓋唔好超過字高 25%。"
placement: behind-subject
difficulty: hard
---

## 效果
超大字放喺人物（或者物件）後面，頭部遮住字嘅一部分，製造前後景深層次，好似雜誌封面。

## 幾時用

開場 hook、關鍵詞（1 秒內），畫面頭頂有空位。

## 幾時唔好用

人物大幅移動、頭髮邊位複雜（摳圖會閃）；字被遮太多會讀唔到，最多遮 30%。

## 參數同節奏


- 字：粗無襯線或粗襯線，闊度約畫面 80%，置於頭頂高度
- 疊層：背景片 → 大字 → 人物前景（有 alpha）
- 字由下升 40px + 淡入 0.35s；細字前導詞 0.15s 前出現


## 實作重點

用 RVM（`tools/relight.py` 同一套摳圖）輸出 alpha 前景：`ffmpeg ... -c:v libvpx-vp9 -pix_fmt yuva420p fg.webm`，喺 HyperFrames 將 fg.webm 疊喺字上面（z-index 較高）。靜止相片可以直接用去背 PNG。

## 已知限制

VP9 alpha 渲染較慢；摳圖邊位要檢查。
