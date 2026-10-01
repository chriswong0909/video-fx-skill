---
id: FX-068
name: 章節導航條
name_en: chapter-nav-bar
category: layout
family: [SP-001]
tags: [chapter, navigation, top-bar, progress]
mood: [clinical, clean, editorial]
fits: [education, medical, podcast-clip, explainer]
video_types: [口播知識, 醫療健康, 訪問對談, 動畫解說]
pace: [中, 慢]
pairs_with: [FX-071, FX-069, FX-070]
conflicts_with: [FX-082]
needs: []
brand_color_ready: true
source: ref16-stroke-talkshow 全片（頂部）
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: "每格 4–7 字；9:16 要縮做 3 格（上一章／本章／下一章）或者改用頂部細進度條，字最少 40px（標籤類 64px 準則以外嘅導航資訊）。"
placement: headroom
aspect: "16:9"
difficulty: easy
component: capsule
entry: []
---

## 效果
畫面頂部一條細長深色半透明橫條，平均分成 4–6 格，每格寫一個章節名（亞裔易中風？／糖尿病與中風／中風先兆……）；講緊嗰章嘅格仔反白或者用品牌色，其他格淡灰。觀眾一眼知道而家講到邊、仲有幾多。

## 幾時用
3 分鐘以上嘅知識／醫療長片、有清楚章節結構嘅訪問；配合章節轉場時跳去下一格。

## 幾時唔好用
60 秒以內短片（冇章節概念）；畫面頂部已經有標題或者頭頂大字嘅鏡頭（會撞）。

## 參數同節奏
- 橫條高 44px（16:9）／56px（9:16），底色 rgba(10,20,40,.55)，每格之間 2px 間隔
- 普通格字色 rgba(255,255,255,.55)，當前格白字 + 底色品牌色或 rgba(255,255,255,.18)
- 換章：舊格 0.25s 淡返灰，新格底色由左向右掃入 0.35s（power2.out）

## 實作重點
整條做一個固定 layer（z-index 高過 #cam），全片 data-duration；換章用 GSAP 喺章節時間點改 class 或者 tween 底色，唔好每章重建元素。

## 已知限制
9:16 頂部 200px 係平台 UI 位，要放喺 200px 以下；字太多會變細到睇唔清，寧願少啲章節。
