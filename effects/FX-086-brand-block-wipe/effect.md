---
id: FX-086
name: 品牌色塊幾何轉場
name_en: brand-block-wipe
category: transition
tags: [brand, geometric, blocks, opening, wipe]
mood: [energetic, bold, modern]
fits: [opening, podcast-clip, brand, interview]
video_types: [訪問對談, 品牌企業, 口播知識, 紀錄 Vlog]
pace: [快]
pairs_with: [FX-061, FX-084, FX-085]
conflicts_with: []
needs: [brand-colors, guest-photos]
brand_color_ready: true
source: ref19-forensic-podcast 0:12–0:27
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: "色塊入面嘅字 2–4 字巨型粗黑，或者頻道名；9:16 色塊改直向排列。"
placement: free
aspect: "16:9"
difficulty: medium
---

## 效果
節目片頭或段落轉換：黑色底上，一堆品牌黃同白嘅長方色塊由唔同方向快速滑入、疊埋、再滑走，中間夾住黑白嘉賓相片同 >>> 箭嘴符號，好似一個有節奏嘅拼圖；最後色塊收埋、露出節目名或者下一個畫面。

## 幾時用
系列節目片頭、嘉賓介紹蒙太奇、長片章節分隔；需要品牌感同節奏感。

## 幾時唔好用
醫療溫和題材（太硬朗）；冇品牌色設定。

## 參數同節奏
- 色塊：品牌色 + #ffffff + #1d1d1d，4–8 塊，每塊 x 或 y 由畫面外滑入 0.3s（expo.out），錯開 0.06s
- 嘉賓相：黑白 filter grayscale(1) contrast(1.1)，放喺色塊之間
- 節拍：每 0.5s 一次重組，配 SFX-002 快速嗖聲
- 收尾：所有色塊同時滑出 0.35s（expo.in），露出下一鏡

## 實作重點
用 GSAP stagger；每塊係絕對定位 div，位置用 grid 計（12 欄）。要做成 clip。

## 已知限制
太多色塊會亂，每一拍最多 6 塊郁。
