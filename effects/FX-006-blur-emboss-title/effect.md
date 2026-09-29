---
id: FX-006
name: 模糊畫面浮雕大字
name_en: blur-emboss-title
category: transition
family: [SP-002, SP-004]
tags: [blur, emboss, big-type, emphasis]
mood: [warm, dramatic, premium]
fits: [talking-head, podcast-clip, medical]
video_types: [口播知識, 醫療健康]
pace: [中, 快]
pairs_with: [FX-005]
conflicts_with: []
needs: []
brand_color_ready: true
source: ref1-glucose-podcast 16:3–17:0（STARCHES）
learned: 2026-09-28
used_in: [doctor2-ref1style, doctor-stairs-breath]
status: active
cjk_fit: good
cjk_notes: "220px 每行最多 4 個字。"
difficulty: easy
---

## 效果
講者畫面 0.3 秒內模糊 + 變暗，上面浮現巨型浮雕字（淺啡色、左上高光、右下深陰影），逐行出現；下一句硬切返清晰畫面。

## 幾時用

結論、呼籲（「盡早搵醫生」），約 1 秒。

## 幾時唔好用

連續用多過一次；字多過兩行。

## 參數同節奏


- wrapper filter: blur(22px) brightness(.55)，0.3s
- 字 260px Serif 900 #c89b6d；text-shadow: -3px -3px 2px rgba(255,235,210,.55), 5px 6px 6px rgba(40,18,6,.8)
- 每行 scale 1.3 → 1、blur 16 → 0，0.4s


## 實作重點

blur 要加喺 `#cam` wrapper，唔好加喺 `<video>`。浮雕字層做 clip。

## 已知限制

軟件渲染 blur 較慢，但 1 秒內冇問題。
