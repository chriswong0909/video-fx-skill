---
id: FX-002
name: 頭像資料卡開場
name_en: profile-hook-card
category: hook
tags: [profile, social, header]
mood: [warm, friendly, editorial]
fits: [talking-head, podcast-clip, medical, education]
pairs_with: [FX-001, FX-009]
conflicts_with: []
needs: [avatar-image]
brand_color_ready: true
source: ref1-glucose-podcast 0:00–3:00
learned: 2026-09-28
used_in: [doctor2-ref1style]
difficulty: easy
---

## 效果
開頭 0–3 秒頂部出現淺色資料卡：圓形頭像（漸變彩環）+ 名稱 + 副標，由上滑入，建立「呢個係邊個」嘅信任感。

## 幾時用
講者／專家口播開場，片長 10–60 秒。

## 幾時唔好用
冇真實帳號／名稱時唔好作假帳號、假追蹤數、假認證剔號；改用中性標題（例如「醫生話你知」）。

## 參數同節奏
- 高 330px，背景 #f6ede4，陰影
- 頭像 196px，conic-gradient 彩環
- 卡 y -330 → 0 0.45s；頭像 back.out 0.4s；文字 stagger 0.15s
- 講完第一句（約 2.7 秒）硬切消失

## 實作重點
頭像用 ffmpeg 由素材截一格臉部：`ffmpeg -ss 1 -i in.mp4 -frames:v 1 -vf crop=360:360:X:Y,scale=240:240 avatar.png`

## 已知限制
會遮住畫面頂部 1/6，鏡頭要推近或下移避免切頭。
