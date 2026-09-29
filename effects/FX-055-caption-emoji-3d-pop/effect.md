---
id: FX-055
name: 字幕旁 3D 小圖示彈出
name_en: caption-emoji-3d-pop
category: accent
family: [SP-003]
tags: [3d-icon, sticker, caption-accent, playful]
mood: [playful, friendly, energetic]
fits: [finance, education, talking-head, lifestyle]
video_types: [口播知識, 訪問對談]
pace: [快, 中]
pairs_with: [FX-052, FX-039]
conflicts_with: []
needs: [3d-icons]
brand_color_ready: true
source: ref9-fire-investment 0:32–0:36
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: 同文字無關；圖示放喺字幕最後一個字右上角。
placement: on-text
difficulty: easy
---

## 效果
字幕出現時，旁邊（通常右上或左下）彈出一個細 3D 小圖示（鈔票、金幣、火箭），貼住關鍵詞，有少少彈跳同旋轉，令名詞更易記。

## 參數同節奏
- 圖示 120–180px，去背 PNG（3D 風格，Higgsfield 生成或圖庫）
- 入場 scale 0 → 1.15 → 1、rotation -20° → 0，0.3s back.out(2.5)
- 停留到該句完結，跟字幕一齊消失

## 實作重點
同一條片圖示風格要一致；每句最多一個。
