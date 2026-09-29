---
id: FX-077
name: 光漏閃光轉場
name_en: light-leak-flash
category: transition
family: [SP-004]
tags: [light-leak, flash, film, transition]
mood: [cinematic, nostalgic, warm]
fits: [storytelling, vlog, documentary, commentary]
video_types: [紀錄 Vlog, 口播知識, 品牌企業, 產品廣告]
pace: [中, 快]
pairs_with: [FX-074, FX-076, FX-049]
conflicts_with: []
needs: [light-leak-overlay]
brand_color_ready: false
source: ref17-hk-retire-north 0:53、ref18-hk-retire-mgmtfee 0:58
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: "冇文字。"
placement: free
aspect: "16:9"
difficulty: easy
---

## 效果
轉場前後，一片橙紅或粉紅光（似舊菲林漏光）由畫面一邊湧入，整個畫面短暫過曝變暖色，約 0.6 秒後褪走，接到下一鏡。

## 幾時用
段落完結、情緒轉換、回憶片段開頭或結尾；配 FX-074 復古調色最夾。

## 幾時唔好用
醫療專業講解中段（太花）；一條片多過 3 次。

## 參數同節奏
- overlay：radial-gradient(circle at 20% 40%, rgba(255,120,60,.95), rgba(255,60,90,.6) 40%, transparent 75%)，mix-blend-mode: screen
- 動畫：opacity 0→1 0.25s，x 位移 -20%→+15% 0.7s，opacity 1→0 0.35s
- 硬切點放喺光最光（約 0.3s）嗰一格

## 實作重點
用 CSS 漸變做就得，唔使素材；或者用有授權嘅 light-leak 片 screen 疊。要做成 clip。

## 已知限制
screen 混合喺好光嘅畫面效果弱，暗畫面先明顯。
