---
id: FX-076
name: 地面透視大字
name_en: ground-perspective-text
category: text-fx
family: [SP-004]
tags: [perspective, 3d-text, ground, keyword]
mood: [dramatic, cinematic]
fits: [storytelling, finance, commentary, b-roll]
video_types: [口播知識, 紀錄 Vlog, 產品廣告]
pace: [中, 快]
pairs_with: [FX-077, FX-074, FX-062]
conflicts_with: [FX-016]
needs: [top-down-footage]
brand_color_ready: true
source: ref17-hk-retire-north 0:52–0:54
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: "3 字以內最有力；serif 900 中文，平躺之後視覺上會變細，字級要比平面大 1.4 倍。"
placement: center
aspect: "16:9"
difficulty: medium
component: headline
entry: [scale]
---

## 效果
一個關鍵詞（無退路）用紅色粗 serif 大字「印」喺地面／枱面上，跟住鏡頭透視平躺（rotateX 約 55°），好似寫喺地上；上面仲有物件跌落（硬幣、錢包），字有少少紙紋質感同陰影。

## 幾時用
結論、警告、情緒最高點；B-roll 係俯拍地面或者枱面時。

## 幾時唔好用
冇平面嘅畫面（人像特寫）；需要清楚閱讀嘅長句。

## 參數同節奏
- 容器 perspective 900px；字 rotateX(55deg) rotateZ(-4deg)
- 字色 #e8494d 帶 12% 白色紋理 mask，text-shadow 0 3px 0 rgba(0,0,0,.35)
- 入場：字由 scale 1.25、opacity 0 壓落 0.25s（back.out），配合物件落地時間
- 之後慢推 1.00→1.05

## 實作重點
透視角度要對準畫面地面消失點，逐鏡試；可同 FX-062 物件跌落疊用。

## 已知限制
透視唔啱會好假，要逐格核對；9:16 地面面積細，字要細啲。
