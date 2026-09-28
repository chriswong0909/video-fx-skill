---
id: FX-009
name: 按句推鏡硬切
name_en: sentence-punch-in
category: camera
tags: [punch-in, reframe, jump-cut, zoom]
mood: [editorial, energetic, warm, clinical]
fits: [talking-head, podcast-clip, medical, education, interview]
pairs_with: [FX-001, FX-002, FX-007, FX-012]
conflicts_with: []
needs: []
brand_color_ready: true
source: ref1-glucose-podcast（整條）+ 原創
learned: 2026-09-28
used_in: [doctor2-editorial, doctor2-ref1style]
difficulty: easy
---

## 效果
單機位口播，每句之間硬切去唔同景別（中景 ↔ 近景），每個鏡頭入面再慢慢推近 3–5%，製造多機位感。

## 幾時用
所有單機位口播，特別係講者佔畫面細（中遠景）時。

## 幾時唔好用
素材解像度低（放大 >2× 會糊）；講者大幅移動。

## 參數同節奏
- 切點：句子邊界（ASR segment 開始），唔好喺詞中間
- 景別交替：例如 1.85 → 2.2 → 1.95；原片講者細時可到 2.2×（1080 源會略軟）
- 每鏡頭 scale +0.06 linear
- transform-origin 對準臉部（例如 540px 660px）；需要頭頂放標題時加 y +150–240

## 實作重點
對 `#camInner` wrapper 做 scale，唔好對 `<video>`。
```
[[start,end,s0,s1,y]].forEach(([a,b,s0,s1,y])=>{tl.set('#camInner',{scale:s0,y},a);tl.to('#camInner',{scale:s1,duration:b-a,ease:'none'},a);});
```

## 已知限制
放大會令畫質變軟；下一步可以考慮 AI 超解像。
