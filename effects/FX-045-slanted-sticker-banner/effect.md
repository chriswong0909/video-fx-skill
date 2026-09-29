---
id: FX-045
name: 斜貼紙警告橫額
name_en: slanted-sticker-banner
category: text-fx
family: [SP-003]
tags: [sticker, warning, cta, tilted]
mood: [urgent, friendly, playful]
fits: [medical, public-health, education]
video_types: [動畫解說, 醫療健康]
pace: [中, 快]
pairs_with: [FX-044, FX-048]
conflicts_with: []
needs: []
brand_color_ready: true
source: ref8-ha-heart-care 0:11.9–0:13.7
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: 原片係中文（廣東話旁白），字體同排版可直接沿用。
difficulty: easy
---

## 效果
一句重點提醒（出現徵狀／一定要及早求醫！）以兩行橙色粗圓體字、厚白描邊、斜 -10°，好似貼紙「啪」一聲貼落喺畫面中間，壓住下面嘅內容。

## 幾時用
每段嘅結論、警告、CTA。

## 參數同節奏
- 字 80–90px 圓體粗字，color #f08a1c，-webkit-text-stroke 14px #fff（paint-order stroke），外加淡陰影
- 入場：scale 1.6 → 1、rotation -18° → -10°，0.25s back.out(2.5)，之後停留
- 可配一下「啪」聲效

## 實作重點
paint-order:stroke fill 令描邊喺字外面，唔會食字。
