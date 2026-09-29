---
id: FX-027
name: 發光漸變關鍵字
name_en: glow-gradient-keyword
category: text-fx
tags: [gradient-text, glow, 3d, cool-tone]
mood: [energetic, modern, premium]
fits: [podcast-clip, talking-head, education, medical]
video_types: [口播知識, 醫療健康]
pace: [快, 中]
pairs_with: [FX-018]
conflicts_with: []
needs: [word-timestamps]
brand_color_ready: true
source: ref4-brain-explainer 0:06–0:07.5、ref5-aging-routine 0:00–0:01.5
learned: 2026-09-29
used_in: [doctor-stairs-breath]
status: active
cjk_fit: good
cjk_notes: "漸變同發光要配 Black 字重先顯；筆畫密要加強 glow 對比。"
placement: inline
difficulty: easy
---

## 效果
兩層字幕嘅冷色版：上下係白色細襯線／無襯線字，重點詞係粗大楷，填色係藍色漸變（淺青 → 深藍）+ 外發光，似金屬或者霓虹，好搶眼。

## 幾時用

深色背景嘅講者（黑、深藍、青綠光）；科技、健康、數字重點（THIRD、BEST!）。

## 幾時唔好用

暖色調片（可改用金橙漸變色，但唔好同冷色混用）。

## 參數同節奏


- 漸變 #7fe3ff → #2b8cff → #1a4fd6；text-shadow 0 0 18px rgba(60,160,255,.55)
- 字 120–150px Sans 900
- 入場：scale 1.3 → 1、blur 8 → 0，0.3s power3.out；可加 0.15s 亮度閃一下


## 實作重點

逐字包 span 用 background-clip:text；glow 用 drop-shadow filter。
