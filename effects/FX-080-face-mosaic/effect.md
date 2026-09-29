---
id: FX-080
name: 面部打格仔
name_en: face-mosaic
category: accent
tags: [mosaic, pixelate, censor, comedy]
mood: [playful, comedic]
fits: [commentary, vlog, storytelling]
video_types: [口播知識, 紀錄 Vlog]
pace: [快, 中]
pairs_with: [FX-075, FX-046]
conflicts_with: []
needs: [face-box]
brand_color_ready: false
source: ref18-hk-retire-mgmtfee 0:16–0:19
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: "冇文字。"
placement: free
aspect: "16:9"
difficulty: medium
---

## 效果
講者講到尷尬、自嘲或者「匿名」位時，佢塊面突然被馬賽克格仔遮住（好似新聞打格），格仔跟住塊面郁，1–3 秒後拎走，製造笑位。

## 幾時用
自嘲、扮路人、講私隱話題嘅搞笑位；真正需要私隱保護嘅路人面孔。

## 幾時唔好用
醫生講專業內容（削弱可信度）；病人真實私隱要用更可靠嘅專業打格方法再人手核對。

## 參數同節奏
- 格仔大小：面闊 1/8（約 24–32px 一格）
- 做法：第二個 <video>（同一原片）縮細到 1/24 再放大，image-rendering: pixelated，用 clip-path 圓角矩形只顯示面部範圍
- 範圍跟 face-box（每 0.2s 一個關鍵點）線性插值
- 入出：硬切，配一聲 SFX-006 或 SFX-013

## 實作重點
face-box 用 lessons/layout-safety.md 嘅 Haar 偵測輸出；兩個 video 要同一 currentTime。

## 已知限制
轉頭太快會露面；正式私隱用途要逐格核對。
