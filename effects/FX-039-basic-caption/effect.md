---
id: FX-039
name: 基本字幕（白字黑光暈）
name_en: basic-caption
category: caption
family: [SP-001, SP-002, SP-003, SP-004, SP-005]
tags: [subtitle, cjk, phrase-sync, clean]
mood: [clean, clinical, neutral]
fits: [talking-head, medical, education, interview, podcast-clip]
video_types: [口播知識, 訪問對談, 醫療健康, 新聞資訊]
pace: [快, 中, 慢]
pairs_with: [FX-017, FX-037, FX-006]
conflicts_with: [FX-051]
needs: [word-timestamps]
brand_color_ready: true
source: original（doctor-stairs-breath 用戶字幕規範）
learned: 2026-09-29
used_in: [doctor-stairs-breath]
status: active
cjk_fit: good
cjk_notes: 為中文而設：按意群 6–12 字一組、80px。
placement: lower
difficulty: easy
---

## 效果
全片唯一一種字幕：思源黑體 Bold 80px 全白，加少量黑色光暈托底；冇底色、冇換色、冇關鍵詞高亮。按意群斷句，一組一行，顯示到下一組出現先換。

## 幾時用

所有冇特效字嘅講嘢位。有特效字（FX-017、FX-037、FX-006、FX-005 等）顯示緊嗰句內容時，**嗰句唔出字幕**，唔好兩樣疊埋。

## 幾時唔好用

同一句已經有特效字；需要強調某個詞（改用特效字，唔好喺字幕入面換色）。

## 參數同節奏


- SansTC 700，80px，#fff；text-shadow 0 0 5px rgba(0,0,0,.45), 0 2px 12px rgba(0,0,0,.5)
- 位置 top 1300px（胸口至枱面），左右各留 60px；一行最多 12 字（960 ÷ 80）
- 斷句：優先喺標點、意群斷；每組 6–12 字；唔好少過 4 字（除非成句就係咁短）
- 入場 opacity + y 10 → 0，0.12s；下一組硬換


## 實作重點

由 ASR 詞語時間合併成意群：累積到 6–12 字或遇到標點就斷；一組嘅結束時間 = 下一組開始時間（或句尾靜音）。書面語轉寫後字數會變，要用轉寫後文字計字數。

## 已知限制

淺色背景（白牆、白底圖）對比度較低，要加強光暈或者避開。
