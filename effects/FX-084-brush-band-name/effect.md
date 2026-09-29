---
id: FX-084
name: 掃筆色帶名牌
name_en: brush-band-name
category: text-fx
family: [SP-003]
tags: [lower-third, name, brush, highlight]
mood: [energetic, bold, youthful]
fits: [interview, podcast-clip, education]
video_types: [訪問對談, 口播知識, 紀錄 Vlog]
pace: [中, 快]
pairs_with: [FX-082, FX-083, FX-085]
conflicts_with: [FX-064, FX-070]
needs: []
brand_color_ready: true
source: ref19-forensic-podcast 0:45–0:51
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: "名 + 身份 6–8 字，粗黑斜體 16:9 約 60px、9:16 最少 110px；中文唔好真斜體，用 skewX(-8deg)。"
placement: lower
aspect: "16:9"
difficulty: easy
---

## 效果
介紹嘉賓時，胸口位先由左向右「掃」出一條黃色粗筆刷色帶（毛邊），跟住黑色粗體斜字（張晏維 法醫）彈出喺色帶上面；停幾秒後色帶由右收走。比普通名牌活潑、年輕。

## 幾時用
年輕、活潑風格嘅訪問或 podcast；YouTube 知識頻道。

## 幾時唔好用
嚴肅醫療機構官方片（用 FX-064 或 FX-070）；同一條片已用其他名牌。

## 參數同節奏
- 色帶：品牌黃 #ffcf2e，SVG 筆刷 mask（兩端毛邊），高度 = 字高 1.5 倍，輕微旋轉 -3°
- 字：#111 900，skewX(-8deg)
- 時序：色帶 clip-path inset(0 100% 0 0)→0 0.3s（power3.out）；字 scale .8→1 + 淡入 0.2s（back.out）
- 收：色帶由右向左收 0.25s，字同時淡出

## 實作重點
筆刷形狀用 SVG path 做 mask（repo 內自製），唔好用第三方筆刷素材。

## 已知限制
黃色喺淺色背景對比弱，要按畫面換品牌色。
