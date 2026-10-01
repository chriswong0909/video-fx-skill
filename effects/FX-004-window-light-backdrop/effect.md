---
id: FX-004
name: 窗光斜影背景
name_en: window-light-backdrop
category: cutaway
family: [SP-002, SP-004]
tags: [background, light, shadow, typography]
mood: [warm, calm, premium]
fits: [podcast-clip, lifestyle, education, medical]
video_types: [口播知識, 產品廣告, 品牌企業]
pace: [中, 慢]
pairs_with: [FX-003]
conflicts_with: []
needs: []
brand_color_ready: true
source: ref1-glucose-podcast 4:00–5:30（方糖）
learned: 2026-09-28
used_in: [doctor2-ref1style]
status: active
cjk_fit: good
difficulty: easy
cjk_notes: ""
style_bound: true
bound_reason: "窗光斜影嘅暖光係效果本身"
component: cutaway
entry: [slide-edge]
---

## 效果
米白底，斜斜嘅窗框陰影慢慢移動，好似陽光照入房；中間放金色大字（可配物件）。

## 幾時用

抽象概念（「運動」「休息」）冇合適畫面時做 1 秒過場，氣氛溫暖。

## 幾時唔好用

需要資訊量大嘅畫面。

## 參數同節奏


- 底色 #efe4d6，右上角 radial 光暈
- 陰影：rotate(-28deg) 嘅 repeating-linear-gradient，陰影位 rgba(120,90,60,.2)，軟邊靠色標漸變做
- 1 秒內 x 移 60px（ease none）


## 實作重點

**唔好喺大元素上用 CSS filter blur**，軟件渲染會出黑塊；軟邊用漸變色標做。要做成 clip。

## 已知限制

冇物件時略空，最好配一個大字標題（例如 FX-017）或者物件。
