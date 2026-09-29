---
id: FX-031
name: 玻璃擬態元件 + 場景
name_en: glass-widget-scene
category: cutaway
tags: [glassmorphism, widget, 3d-scene, calendar]
mood: [aspirational, modern, dreamy]
fits: [creator, lifestyle, product, education]
video_types: [品牌企業, 口播知識]
pace: [中]
pairs_with: [FX-030, FX-035, FX-033]
conflicts_with: [FX-015, FX-041]
needs: [scene-image]
brand_color_ready: true
source: ref6-ai-creator 0:00.5–0:04
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
difficulty: medium
cjk_notes: ""
---

## 效果
一張夢幻場景相（花海、草地、天空，常用 AI 生成）做背景，前面浮住一個毛玻璃效果嘅 UI 元件（日曆 July 01），上面有大字漸變數字（2025）同細字，慢慢推近。

## 幾時用

講「新開始」「每個星期」「時間」；想要高質、夢幻感。

## 參數同節奏


- 玻璃卡：background rgba(255,255,255,.18)、backdrop-filter blur(18px)、1px 白邊 .35
- 大字：漸變 #c9b8ff → #7c6cf0，160px
- 背景慢推 scale 1 → 1.06（整段）；卡片由下浮上 0.5s


## 實作重點

backdrop-filter 喺軟件渲染可能慢／唔支援：可以預先將背景模糊一份做卡片底圖代替。
