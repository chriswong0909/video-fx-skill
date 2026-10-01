---
id: FX-065
name: 金句雙色重點字
name_en: key-quote-twotone
category: text-fx
family: [SP-002, SP-005]
tags: [quote, highlight, two-tone, interview]
mood: [inspiring, journalistic, clear]
fits: [interview, documentary, medical, education]
video_types: [訪問對談, 紀錄 Vlog, 新聞資訊]
pace: [慢, 中]
pairs_with: [FX-064, FX-039]
conflicts_with: [FX-052]
needs: [word-timestamps]
brand_color_ready: true
source: ref14-reporter-baseball 0:13、0:22、0:44、1:11、1:36、2:06
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: 為中文設計：每行 4–8 字，最多 3 行。
placement: center
difficulty: easy
component: headline
entry: [rise]
---

## 效果
受訪者講出金句時，胸口位置出現 2–3 行粗大字：一般字白色、重點字黃色（#ffd400），每行有黑色半透明底條（或粗黑描邊）；同時細字幕照常。每條片只用喺 3–6 句最重要嘅說話。

## 幾時用
訪問、紀錄片，用嚟標記核心訊息，令觀眾靜音都睇得明主旨。

## 參數同節奏
- 字 64–76px Sans 900；白 #fff／黃 #ffd400；每行底條 rgba(0,0,0,.72)，padding 4px 14px（或 6px 黑描邊冇底條）
- 入場：逐行由下升 + opacity，0.2s，stagger 0.12s；停留到句尾 + 0.5s
- 引號版本：「我做到了！」用黃底黑字方框

## 實作重點
金句時細字幕（FX-039）可以照出，但要放遠啲避免重疊。
