---
id: FX-013
name: 問題浮動符號 + 紅標籤
name_en: question-float-label
category: text-fx
family: [SP-002]
tags: [question, label, top-title, decorative]
mood: [warm, playful, editorial]
fits: [podcast-clip, education, medical]
video_types: [口播知識]
pace: [快, 中]
pairs_with: []
conflicts_with: []
needs: [face-box]
brand_color_ready: true
source: ref1-glucose-podcast 10:0–11:5（GIVE YOUR BODY）
learned: 2026-09-28
used_in: [doctor2-ref1style]
status: active
cjk_fit: adjust
cjk_notes: "超大字改黑體 Black 比襯線清楚。"
placement: headroom
difficulty: easy
component: capsule
entry: [rise]
---

## 效果
講者頭頂：細字 + 超大深紅粗襯線字 + 下面紅底白字小標籤；兩邊有橙色問號彈出並慢慢上下浮動。

## 幾時用

講者提出問題或「原因係…」嘅轉折句。

## 參數同節奏

紅字 130px #8e241f；標籤 #9e2b25 54px；問號 120–150px #e98a2e，back.out(2) 彈入，之後 1.2–1.4s sine 浮動

## 實作重點

問號要有 z-index 高過 #cam，否則會被遮。講者要推近兼下移留頭頂位。
