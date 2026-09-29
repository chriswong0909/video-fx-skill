---
id: FX-074
name: 復古菲林暗角調色
name_en: vintage-film-grade
category: grade-light
family: [SP-004]
tags: [film, grain, vignette, retro, grade]
mood: [nostalgic, cinematic, moody]
fits: [documentary, finance, storytelling, b-roll]
video_types: [口播知識, 紀錄 Vlog, 新聞資訊]
pace: [中, 快, 慢]
pairs_with: [FX-072, FX-073, FX-077, FX-078]
conflicts_with: [FX-015]
needs: []
brand_color_ready: false
source: ref17-hk-retire-north 0:10–0:53、ref18-hk-retire-mgmtfee 全片 B-roll
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: "唔影響文字；疊喺字幕之下。"
placement: free
aspect: "16:9"
difficulty: easy
---

## 效果
所有 B-roll 加一層舊菲林質感：黑位提起、對比降低、輕微偏暖黃、四角深暗角、細顆粒噪點，偶爾輕微閃光。講者鏡頭保持乾淨，B-roll 就變成「回憶／新聞片段」感，兩者一睇就分得開。

## 幾時用
大量用舊片、新聞片、生活片段做 B-roll 嘅評論片；想統一唔同來源素材嘅色調。

## 幾時唔好用
醫療專業內容要準確顏色（皮膚、傷口、化驗）；已經用暖色 podcast 調色 FX-015 嘅講者鏡頭。

## 參數同節奏
- filter：contrast(.88) saturate(.8) sepia(.18) brightness(.96)
- 暗角：radial-gradient(ellipse, transparent 55%, rgba(0,0,0,.55) 100%)
- 顆粒：SVG feTurbulence noise，opacity .10，每 2 幀換 seed（或預渲染 grain.mp4 疊 overlay）
- 偶發閃光：每 3–5 秒 brightness 1.08 閃 2 幀

## 實作重點
filter 做喺 B-roll wrapper；暗角同顆粒係獨立 layer，只喺 B-roll clip 時間出現。顆粒用預渲染小片 loop 最穩陣（軟件渲染 feTurbulence 慢）。

## 已知限制
顆粒太強壓縮後會變糊，opacity 唔好超過 .12。
