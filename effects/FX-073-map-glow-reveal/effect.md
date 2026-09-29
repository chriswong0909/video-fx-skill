---
id: FX-073
name: 地圖掃入發光
name_en: map-glow-reveal
category: cutaway
tags: [map, reveal, glow, location]
mood: [dramatic, editorial]
fits: [news, finance, documentary, explainer]
video_types: [新聞資訊, 口播知識, 紀錄 Vlog]
pace: [中, 快]
pairs_with: [FX-074, FX-072, FX-050]
conflicts_with: []
needs: [map-svg]
brand_color_ready: true
source: ref17-hk-retire-north 0:23–0:28
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: "地圖上嘅標註字 2–5 字，serif 粗體，9:16 最少 72px。"
placement: center
aspect: "16:9"
difficulty: medium
---

## 效果
背景片轉暗轉糊，一幅紅色地圖由一條發光掃描線從左向右掃出嚟（邊緣火紅光），掃完地圖微微發光，目標城市位置閃一點黃光，旁邊出一行標註字（⅓香港生活費）。

## 幾時用
講到地區、遷移、分佈（北上退休、病例集中區、醫院分佈）。

## 幾時唔好用
地圖邊界有政治敏感或者唔準確嘅時候（要用官方地圖）；冇地理概念嘅內容。

## 參數同節奏
- 背景：原片 blur 8px + brightness .55
- 地圖：SVG path，fill #e3120b，filter drop-shadow(0 0 18px rgba(255,60,20,.6))
- 掃入：clip-path inset(0 100% 0 0)→inset(0 0 0 0) 0.8s + 一條 6px 橙黃光條跟住邊緣移動
- 目標點：黃色圓點 scale 0→1 + 脈衝一次；標註字 0.2s 後淡入上移 20px

## 實作重點
地圖 SVG 用有授權嘅公開地圖（例如 Natural Earth），唔好自己畫邊界；光條同 clip 用同一條 GSAP timeline 同步。

## 已知限制
地圖邊界準確性要使用者確認；香港本地題材可改用 18 區地圖。
