---
id: FX-017
name: 頭頂大字（無襯線）
name_en: top-headline-sans
category: text-fx
tags: [kinetic-type, sans, headroom, word-sync]
mood: [energetic, clean, modern]
fits: [talking-head, fitness, podcast-clip, education]
video_types: [口播知識]
pace: [快]
pairs_with: [FX-018, FX-019]
conflicts_with: []
needs: [word-timestamps, face-box]
brand_color_ready: true
source: ref2-fitness-bloodsugar 0:00–0:02.5, 0:06–0:07.5
learned: 2026-09-29
used_in: [doctor-stairs-breath]
status: active
cjk_fit: adjust
cjk_notes: "英文一個大詞約等於中文 2–4 字；細字最少 76px；大字 6 個字以上減到 140px。"
placement: headroom
difficulty: easy
---

## 效果
講者頭頂空位：一行細白字逐詞出（靠左），然後一個超大粗白色無襯線字（幾乎全闊）砸落，下面再跟細字。字幕喺頭頂，唔遮臉同手勢。

## 幾時用

講者畫面頂部有空位（牆、背景）；想要現代、直接嘅感覺。

## 幾時唔好用

頂部背景太光（白字睇唔清，要加陰影）；頂部已有其他標題（例如 FX-059）。

## 參數同節奏


- 細字 76–80px Sans 500，白色，陰影
- 大字 170–200px Sans 900，字距 -2px，陰影 0 6px 24px rgba(0,0,0,.35)
- 大字：scale 1.15 → 1、opacity 0 → 1，0.22s power4.out（要快）
- 一句一組，硬切


## 實作重點

位置 top 120–260px；大字 `white-space:nowrap` + 自動縮字（字數多時減字號）。

## 已知限制

中文大字 6 個字以上要減到 140px。
