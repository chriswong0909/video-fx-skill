---
id: FX-040
name: 平滑推鏡
name_en: smooth-punch
category: transition
tags: [camera, punch-in, ease, talking-head]
mood: [clean, editorial, calm]
fits: [talking-head, medical, education, interview, podcast-clip]
video_types: [口播知識, 訪問對談, 醫療健康]
pace: [中, 慢]
pairs_with: [FX-039, FX-017]
conflicts_with: []
needs: [face-box]
brand_color_ready: true
source: original（doctor-stairs-breath：用戶話硬剪感太強）
learned: 2026-09-29
used_in: [doctor-stairs-breath]
status: active
cjk_fit: good
cjk_notes: 同文字無關。
placement: layout
difficulty: easy
---

## 效果
單機位口播由一個機位用 0.24 秒順滑推去另一個機位（例如闊鏡 → 中鏡），代替硬切；推完之後鏡內繼續慢推 3%。

## 幾時用

重點句開始、段落轉換、開場大字之後第一句。每 20 秒約 1 次。

## 幾時唔好用

連續多句都用（會似暈船）；兩個機位差距少過 1.3 倍（硬切或者平滑都唔明顯）。

## 參數同節奏


- 固定機位：闊 1.0／中 1.3／特寫 1.7；推鏡中心 = 眼睛高度（例：540px 640px）
- 平滑段：0.24 秒 power2.inOut，由切點前 0.12 秒開始
- 配輕聲 swish 聲效


## 實作重點

用 #camInner wrapper（#cam > #camInner > video）；推鏡中心固定，唔好逐鏡改，否則眼睛位置會跳。

## 已知限制

特寫超過 1.7 倍（1080 原片）會開始模糊。
