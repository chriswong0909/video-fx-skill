---
id: FX-078
name: 撕紙剪報 + 螢光筆
name_en: torn-paper-clipping
category: cutaway
family: [SP-005]
tags: [news-clipping, highlight, paper, evidence]
mood: [editorial, journalistic, handmade]
fits: [news, finance, commentary, medical]
video_types: [新聞資訊, 口播知識, 醫療健康]
pace: [中, 慢]
pairs_with: [FX-079, FX-074, FX-081, FX-041]
conflicts_with: [FX-058]
needs: [article-screenshot]
brand_color_ready: true
source: ref18-hk-retire-mgmtfee 0:12–0:27
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: "新聞截圖本身係中文；螢光筆只劃 1–2 句重點，字要大到 9:16 縮圖睇得清（截圖放大到畫面闊 110% 再慢移）。"
placement: layout
aspect: "16:9"
difficulty: medium
style_bound: true
bound_reason: "剪報紙色同螢光筆黃係效果本身"
component: cutaway
entry: [rise, scale]
---

## 效果
引用新聞或研究時，切去一張皺白紙：上面貼住新聞網頁截圖（標題、來源 logo、內文），紙邊係撕爛嘅毛邊；跟住螢光筆（黃、粉紅）由左向右逐句劃過重點，鏡頭慢慢移去被劃嗰句。

## 幾時用
引用新聞、官方數據、研究結論，增加可信度；醫療片引用衞生署或期刊。

## 幾時唔好用
冇真實來源（唔好偽造新聞截圖）；截圖字太細、太長。

## 參數同節奏
- 紙：#f4f2ee + 皺紋紋理，上下邊撕紙 SVG mask，陰影 0 10px 30px rgba(0,0,0,.4)
- 截圖 multiply 疊喺紙上（似印刷）
- 螢光筆：黃 rgba(255,230,0,.75)、粉 rgba(255,60,160,.6)，高度 = 行高 90%，scaleX 0→1 由左至右 0.45s／行，行與行之間 0.1s
- 鏡頭：整張紙 y 慢移 + scale 1.00→1.08，對準劃重點嗰行

## 實作重點
螢光筆係 mix-blend-mode: multiply 嘅色塊，放喺截圖上面；位置用截圖像素座標寫死。來源寫喺字幕或角落註腳。

## 已知限制
只可以用真實截圖，唔好改內容；網站 logo 屬第三方，只作引用。
