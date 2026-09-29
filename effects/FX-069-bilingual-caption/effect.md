---
id: FX-069
name: 中英雙語字幕
name_en: bilingual-caption
category: caption
family: [SP-001]
tags: [caption, bilingual, english, subtitle]
mood: [clean, trustworthy, international]
fits: [interview, medical, education, podcast-clip]
video_types: [訪問對談, 醫療健康, 口播知識, 新聞資訊, 品牌企業]
pace: [慢, 中]
pairs_with: [FX-068, FX-070, FX-071]
conflicts_with: [FX-039, FX-051, FX-060]
needs: [word-timestamps, english-translation]
brand_color_ready: false
source: ref16-stroke-talkshow 全片
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: "中文 80px 白字粗黑 + 英文 52px（註腳最細準則）細一級、白色 85% 透明度；兩行置中；英文唔好超過畫面闊 86%，長句自動縮到 46px 為止。"
placement: lower
aspect: "16:9"
difficulty: easy
---

## 效果
上行中文、下行英文嘅雙語字幕：中文較大較粗，英文細一級、較淡，兩行都係白字加柔和黑陰影，冇底色，置中喺畫面下方。屬「基本字幕」類，全片只揀一款（同 FX-039／FX-051 二揀一）。

## 幾時用
面向海外觀眾、機構或醫院官方片、社區教育片；講者講廣東話但要照顧唔識中文嘅觀眾。

## 幾時唔好用
快節奏短片（兩行字太多，追唔切）；已經有好多特效字嘅畫面。

## 參數同節奏
- 中文 80px（9:16）／44px（16:9）Noto Sans TC 700，英文約中文 0.62 倍，行距 1.15
- 陰影 0 2px 8px rgba(0,0,0,.55)，冇描邊
- 位置：9:16 底部安全區以上（bottom 380px），16:9 約畫面 88% 高度
- 換句硬切，唔加動畫；中英同步出同步收

## 實作重點
字幕 JSON 每組多一個 en 欄位；翻譯要人手核對（醫學名詞尤其重要）。同 FX-039 共用斷句邏輯。

## 已知限制
英文翻譯要使用者確認；兩行字佔位高，面部禁區要預留多一行位。
