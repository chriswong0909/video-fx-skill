---
id: FX-066
name: 大數字逐位打出
name_en: number-type-reveal
category: list-chart
family: [SP-001, SP-005]
tags: [number, stat, count, typewriter]
mood: [clean, journalistic, confident]
fits: [news, education, data, medical]
video_types: [新聞資訊, 口播知識, 醫療健康]
pace: [中, 慢]
pairs_with: [FX-067, FX-034]
conflicts_with: []
needs: []
brand_color_ready: true
source: ref15-reporter-ivod 1:44–1:46
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: 數字後面跟一行 24–40px 中文說明（最多 8 字）。
placement: headroom
difficulty: easy
---

## 效果
講者旁邊或頭頂空位出現一個超大白色數字，逐位打出（4 → 45 → 455），打完加單位（「則」）同下面一行細字說明（議題關鍵字），乾淨利落。

## 幾時用
數據、統計、研究結果；背景要乾淨（淺灰牆最好）。

## 參數同節奏
- 數字 180–220px Sans 900（或 IBM Plex Mono）白色／深灰（跟背景）；單位 60px
- 逐位：每位相隔 0.12s（用 textContent set，唔好用 counter 小數）
- 說明文字 0.2s 後淡入

## 實作重點
數字要有出處；大於 4 位數加千位逗號。
