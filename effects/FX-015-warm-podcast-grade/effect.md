---
id: FX-015
name: 暖色 podcast 調色
name_en: warm-podcast-grade
category: grade-light
tags: [color-grade, warm, ffmpeg]
mood: [warm, cozy, editorial]
fits: [podcast-clip, talking-head, lifestyle]
video_types: [口播知識, 訪問對談, 紀錄 Vlog]
pace: [中, 慢]
pairs_with: [FX-003, FX-004]
conflicts_with: []
needs: []
brand_color_ready: true
source: ref1-glucose-podcast（整體色調）
learned: 2026-09-28
used_in: [doctor2-ref1style]
status: active
cjk_fit: good
difficulty: easy
---

## 效果
整體偏桃杏暖色、輕微降飽和、黑位微提，加四角暖啡暈影，似 ref1 嘅 podcast 色調。

## 參數同節奏

ffmpeg：
`colorbalance=rs=0.05:gs=0.01:bs=-0.06:rm=0.05:bm=-0.05:rh=0.03:bh=-0.03,eq=contrast=1.06:saturation=0.92:gamma=0.98,curves=all='0/0.03 0.5/0.49 1/0.96'`
HTML 暈影：radial-gradient(… rgba(90,50,30,.28))

## 實作重點

渲染前用 ffmpeg 處理素材（`-g 15` 方便 seek）。

## 已知限制

原片偏冷白光時效果有限。
