---
id: FX-071
name: 解說畫板 + 講者畫中畫
name_en: explainer-board-pip
category: layout
tags: [explainer, pip, 3d-animation, board, medical]
mood: [clinical, clean, educational]
fits: [medical, education, interview, podcast-clip]
video_types: [醫療健康, 動畫解說, 口播知識, 訪問對談]
pace: [慢, 中]
pairs_with: [FX-068, FX-069, FX-028, FX-021]
conflicts_with: [FX-003, FX-053]
needs: [3d-animation-or-photo, speaker-footage]
brand_color_ready: true
source: ref16-stroke-talkshow 0:20–1:03
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: "主題標籤 4–8 字，16:9 約 22px 粗體、9:16 最少 64px；字幕照放畫板下面。"
placement: layout
aspect: "16:9"
difficulty: medium
---

## 效果
講解原理時，整個畫面轉做淺藍紙紋底：左上一塊大圓角畫板播 3D 醫學動畫（腦、血管、血球），右下角一個細畫中畫繼續播講者（同主持切換都得），畫板左下角貼一個白色主題標籤「什麼是中風？」，兩個角落有淡藍斜色塊點綴。講者聲音唔斷，觀眾睇圖同時見到人。

## 幾時用
醫生講解病理、機制、流程，有 3D 動畫或示意片可以放；想保留講者存在感但畫面主角係圖。

## 幾時唔好用
冇合適素材（得張細圖撐唔起大畫板）；純情緒、故事位（應該睇人）。

## 參數同節奏
- 底色 #e8f3f8 + 淡紙紋，角落色塊 #bcd9f0 旋轉 -18°
- 畫板：16:9 約 78% 闊、圓角 10px、陰影 0 12px 30px rgba(20,60,100,.25)；9:16 改為上半部 92% 闊、4:5 比例
- 畫中畫：畫板闊 30%，白邊 4px、圓角 6px，右下疊住畫板角 6%
- 入場：畫板由 scale .94 + 淡入 0.5s；畫中畫遲 0.2s 由右下滑入；標籤 0.15s 後彈出
- 畫板內素材每 3–5 秒換鏡，慢推 1.00→1.06

## 實作重點
畫板同畫中畫都係 clip（全屏 layer）；畫中畫用第二個 <video>（同一原片，同步時間），filter 做喺 wrapper。3D 動畫用 Higgsfield generate_video 或 Canva 圖庫片，醫學內容標明需醫生審核。

## 已知限制
要有質素好嘅 3D／示意素材先靚；9:16 空間細，畫中畫要縮到約 34% 闊並避開字幕位。
