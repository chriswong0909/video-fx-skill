---
id: FX-070
name: 大字英文名 + 膠囊職銜
name_en: bigname-pill-title
category: text-fx
tags: [lower-third, name, title, pill]
mood: [clean, modern, trustworthy]
fits: [interview, medical, podcast-clip]
video_types: [訪問對談, 醫療健康, 品牌企業, 新聞資訊]
pace: [中, 慢]
pairs_with: [FX-069, FX-068, FX-039]
conflicts_with: [FX-064, FX-084]
needs: []
brand_color_ready: true
source: ref16-stroke-talkshow 0:08–0:17
learned: 2026-09-29
used_in: []
status: active
cjk_fit: adjust
cjk_notes: "原片英文名全大寫粗體；中文名用 Noto Sans TC 900、字距 0.02em，4 字以內；職銜膠囊 36–40px（16:9）／64px（9:16）。"
placement: lower
aspect: "16:9"
difficulty: easy
---

## 效果
受訪者第一次出現時，胸口左邊先滑入一個藍色圓角膠囊（白字職銜：東華醫院藥劑部主管），跟住上面由下向上抹出一行超大白色粗體名字（GINA YAM）；停 5–8 秒後一齊收走。比 FX-064 更大、更有節目感。

## 幾時用
訪問節目、醫生／專家首次出場；想名字夠醒目、似電視台清談節目。

## 幾時唔好用
已經用 FX-064 或 FX-084 嘅片（同一條片名牌只用一款）；講者位置喺畫面左下（會遮身）。

## 參數同節奏
- 名字：白色 900 粗體，16:9 約 64px、9:16 約 120px，輕微陰影
- 膠囊：品牌色（原片 #2a6be0）底、圓角 6px、白字 500，左右 padding 16px
- 時序：膠囊 x -40→0 + 淡入 0.3s；0.15s 後名字 clip-path 由下向上 0.35s（power3.out）
- 收：名字同膠囊一齊淡出 0.25s

## 實作重點
名字同膠囊放同一 group，left 對齊；名字用 clip-path inset 做抹出，唔好用 scale（字會糊）。

## 已知限制
英文名效果最好；中文長名（5 字以上）會太闊，要縮字。
