---
id: FX-064
name: 人名職銜名牌
name_en: name-lower-third
category: text-fx
family: [SP-001, SP-005]
tags: [lower-third, name, title, interview]
mood: [clean, trustworthy, journalistic]
fits: [interview, documentary, medical, news]
video_types: [訪問對談, 新聞資訊, 醫療健康]
pace: [慢, 中]
pairs_with: [FX-065, FX-039, FX-051, FX-058]
conflicts_with: []
needs: []
brand_color_ready: true
source: ref14-reporter-baseball 0:02–0:20
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: 名 36–40px 粗、職銜 22–26px；職銜長就縮字唔好斷行。
placement: lower
difficulty: easy
component: capsule
entry: [draw]
---

## 效果
受訪者第一次出現時，胸口位置出現一個白色半透明細名牌：左邊一條品牌色直條，右邊上行粗體人名、下行細字職銜；停留 3–5 秒後收走。

## 幾時用
所有訪問片、醫生講解（醫生名 + 專科 + 機構），建立可信度。

## 參數同節奏
- 名牌：白 rgba(255,255,255,.92)，高 90px，padding 10px 20px 10px 26px；左直條 8px 品牌色（例 #1f6fd6）
- 名 40px Sans 900 #111；職銜 24px Sans 500 #333
- 入場：直條 scaleY 0 → 1（0.15s），再名牌由左滑出 clip-path（0.25s）；出場反向

## 實作重點
只喺第一次出現同長時間冇出現後再出；唔好遮住手勢。
