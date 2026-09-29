---
id: FX-018
name: 單字跳字幕
name_en: single-word-pop
category: text-fx
family: [SP-003]
tags: [word-by-word, minimal, sans, karaoke]
mood: [clean, energetic, modern]
fits: [talking-head, podcast-clip, interview, education, medical]
video_types: [口播知識, 訪問對談]
pace: [快]
pairs_with: [FX-017, FX-027]
conflicts_with: []
needs: [word-timestamps, face-box]
brand_color_ready: true
source: ref2 0:12–0:14、ref4 0:13、ref5 0:11–0:14、ref3 0:10.5
learned: 2026-09-29
used_in: []
status: active
cjk_fit: poor
cjk_notes: "英文逐詞跳；中文 2–4 字一組會好碎。唔好做基本字幕（用 FX-039）；做特效字時每組最少 4 字、按意群斷。"
placement: lower
difficulty: easy
---

## 效果
講者胸口位置，每次只顯示一個（或兩個）詞，白色粗無襯線，跟住講嘢逐個換，冇底框。最簡單但最耐睇嘅口播字幕。

## 幾時用

過場之間嘅普通句子、收尾；配合其他大型效果做「休息位」。

## 幾時唔好用

需要觀眾讀完整句（例如數據、步驟）。

## 參數同節奏


- 76–84px Sans 700，白色，陰影 0 2px 10px rgba(0,0,0,.5)
- 每詞：scale 0.92 → 1 + opacity，0.08s；下一詞硬換
- 重點詞可轉斜體或者換色（見 FX-027）


## 實作重點

由 ASR 詞語時間直接生成；中文每組最少 4 字、按意群斷；唔好做基本字幕（用 FX-039）。
