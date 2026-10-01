---
id: FX-046
name: 動態模糊橫掃切換
name_en: motion-blur-whip
category: transition
family: [SP-003]
tags: [whip, blur, carousel, swap]
mood: [energetic, friendly]
fits: [education, explainer, medical, product]
video_types: [動畫解說, 口播知識]
pace: [中, 快]
pairs_with: [FX-041, FX-048, FX-047]
conflicts_with: []
needs: []
brand_color_ready: true
source: ref8-ha-heart-care 0:20.0–0:22.2
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: 原片係中文（廣東話旁白），字體同排版可直接沿用。
difficulty: easy
component: camera
entry: [blur]
---

## 效果
一組插圖逐個換（飲食均衡 → 勤做運動 → 戒煙……），舊圖向左急速滑走、新圖由右邊急速滑入，過程中加橫向動態模糊，標籤字同步換。標題固定唔郁。

## 幾時用
列舉 3–6 項建議／步驟，每項 3–4 秒。

## 參數同節奏
- 過場 0.35s：舊圖 x 0 → -900、新圖 x 900 → 0，ease power3.inOut
- 模糊：過場中段 filter blur(18px)，兩頭 0（用 keyframes 或者兩段 tween）
- 標籤：舊標籤淡走 0.15s，新標籤 0.2s 後升上

## 實作重點
blur 做喺圖片 wrapper；每項做 clip 或者用 x 推走（唔好只用 opacity 切全屏層）。
