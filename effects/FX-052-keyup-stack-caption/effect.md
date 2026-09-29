---
id: FX-052
name: 大字疊行 Keyup 字幕
name_en: keyup-stack-caption
category: text-fx
tags: [kinetic-type, stacked, keyup, cjk]
mood: [energetic, bold, modern]
fits: [talking-head, finance, education, podcast-clip]
video_types: [口播知識, 訪問對談]
pace: [快]
pairs_with: [FX-053, FX-055]
conflicts_with: [FX-039, FX-051]
needs: [word-timestamps]
brand_color_ready: true
source: ref9-fire-investment 0:00–0:04
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: 為中文設計：2–4 個字一行，疊 2–3 行，每行大細唔同。
placement: center
difficulty: easy
---

## 效果
講者胸口位置，每句拆成 2–3 行疊起嘅超大白色粗黑體字（例如「想／財務／自由」），行與行大細唔同（重點行最大），字有黑色描邊陰影；逐行「key up」彈出，一句完即換。取代普通字幕，全片每句都係大字。

## 幾時用
快節奏口播、理財／知識 Reels，想每句都有衝擊力。

## 幾時唔好用
慢節奏訪問、醫療嚴肅內容（太吵）；同 FX-039／FX-051 基本字幕唔好同時出。

## 參數同節奏
- 字：Noto Sans TC 900，重點行 150–170px、其餘 100–120px；白字 + 6px 黑描邊（paint-order stroke）+ 陰影
- 行：每行 2–4 字，置中，行距 0.95
- 入場：每行 scale 1.25 → 1 + opacity，0.12s，行與行相隔 0.08s；可加輕微斜字（skew -6°）做強調
- 每句 1–1.8 秒，硬切

## 實作重點
由 ASR 按意群斷，再按字數分行（重點詞獨立一行放大）。
