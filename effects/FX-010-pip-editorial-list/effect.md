---
id: FX-010
name: 相框加清單版面
name_en: pip-editorial-list
category: layout
family: [SP-001]
tags: [pip, list, editorial, numbered]
mood: [clinical, editorial, clean]
fits: [medical, education, talking-head]
video_types: [醫療健康, 口播知識]
pace: [中, 慢]
pairs_with: []
conflicts_with: [FX-005, FX-038, FX-024]
needs: [list-content]
brand_color_ready: true
source: original（doctor2-editorial）
learned: 2026-09-28
used_in: [doctor2-editorial]
status: active
cjk_fit: good
cjk_notes: "清單字最少 72px；編號可保留拉丁斜體數字。"
placement: layout
difficulty: medium
component: frame
entry: [scale, slide-edge]
---

## 效果
講到列舉時，講者畫面縮入頂部圓角相框（品牌色邊框 + 小色塊），下面米白底逐條彈出編號清單（01/02/03，數字斜體品牌色，後面小黃色塊）。講者全程見到，原聲不斷。

## 幾時用

要保留講者但又要展示 2–4 項清單；醫療／專業內容。

## 幾時唔好用

想要 ref1 式全屏畫廊（用 FX-005）。

## 參數同節奏


- #cam：scale .62、y -100、clipPath inset(250px 90px 670px 90px round 58px)，0.55s power3.inOut
- 相框 570×632 描邊 6px 品牌色
- 每行 190px 高；數字 Playfair Italic 104px；文字 Serif 900 100px
- 返回：反向 tween 0.45s


## 實作重點

遮罩底色（#shade 漸變）要等相框完全還原先顯示，否則會喺米白底見到灰色漸變。

## 已知限制

返回全屏嗰 0.3 秒，白色字幕會疊喺米白底上面難睇。
