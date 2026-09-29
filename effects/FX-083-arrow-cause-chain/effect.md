---
id: FX-083
name: 箭嘴因果鏈
name_en: arrow-cause-chain
category: text-fx
family: [SP-001, SP-003, SP-005]
tags: [arrow, cause-effect, keyword, logic]
mood: [educational, energetic, clear]
fits: [education, medical, commentary, podcast-clip]
video_types: [口播知識, 醫療健康, 動畫解說, 訪問對談]
pace: [中, 快]
pairs_with: [FX-082, FX-084, FX-039]
conflicts_with: [FX-065]
needs: []
brand_color_ready: true
source: ref19-forensic-podcast 0:37–0:41
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: "每節 3–6 字，最多 3 節；16:9 約 56px、9:16 最少 96px（特效細字 72px 以上）；9:16 改為上下直排箭嘴。"
placement: lower
aspect: "16:9"
difficulty: easy
---

## 效果
講者講「由 A 推到 B」嗰種因果時，畫面左下出一行粗體白字（屍體的傷口），跟住一個箭嘴「➔」畫出，再出第二節黃字（死者生前遭遇）；字有黑色粗描邊同陰影，逐節出、配合講者語速。

## 幾時用
因果、推論、流程（高血壓 → 血管硬化 → 中風）；醫療知識片好好用。

## 幾時唔好用
超過 3 節（改用清單 FX-032／FX-067）；純情緒句子。

## 參數同節奏
- 字：Noto Sans TC 900，白 / 品牌黃 #ffcf2e，描邊 6px #111（paint-order stroke）+ 陰影 0 4px 0 rgba(0,0,0,.4)
- 箭嘴：SVG 線 + 箭頭，stroke-dashoffset 畫出 0.25s
- 時序：第一節 x -20→0 淡入 0.25s；箭嘴；第二節 0.25s；對準講者講到嗰個詞
- 收：一齊淡出 0.2s

## 實作重點
每節獨立 span；時間用 word timestamps 對準關鍵詞。9:16 用 flex-direction column + 箭嘴轉 90°。

## 已知限制
同字幕同時出現時要避免重疊（放喺字幕上方 1.5 行）。
