---
id: FX-075
name: 暫停符號故障
name_en: pause-icon-glitch
category: accent
tags: [pause, icon, glitch, stop]
mood: [dramatic, playful, energetic]
fits: [storytelling, finance, commentary]
video_types: [口播知識, 新聞資訊, 紀錄 Vlog]
pace: [快, 中]
pairs_with: [FX-054, FX-074, FX-046]
conflicts_with: []
needs: []
brand_color_ready: false
source: ref17-hk-retire-north 0:38–0:41
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: "冇文字；字幕照常。"
placement: center
aspect: "16:9"
difficulty: easy
---

## 效果
講者講「慢著／等等」嗰刻，畫面定格轉糊，正中彈出一個大白色暫停符號（圓圈 + 兩條直槓），邊緣有 RGB 錯位同橫向故障切片，約 2 秒後故障一下消失，接住轉話題。

## 幾時用
轉折位：「但係……」「慢著」「先停一停」；推翻前面講法之前。

## 幾時唔好用
嚴肅病情；一條片用多過一次。

## 參數同節奏
- 符號：直徑 16:9 約 280px／9:16 約 420px，白圈 22px 粗，兩槓各 46×150px
- 入場：scale 1.3→1 + 淡入 0.2s；背景 blur 10px、brightness .7
- 故障：每 0.4s 隨機 2–3 條 clip-path 橫切片 x 位移 ±12px 持續 2 幀；紅青 text-shadow ±4px
- 出場：最後 0.3s 故障加劇後消失

## 實作重點
背景定格：用 video 暫停（tl 設 currentTime 固定）或者截圖做靜態 layer；符號用純 CSS／SVG。

## 已知限制
唔好同 FX-054 喺相近位置一齊用，會太亂。
