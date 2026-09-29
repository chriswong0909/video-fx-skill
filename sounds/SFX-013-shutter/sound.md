---
id: SFX-013
name: 相機快門
name_en: Camera shutter
category: foley
duration: 0.30
volume: 0.45
mood: [高級編輯感, 溫暖生活]
video_types: [口播知識, 訪問對談, 醫療健康, 動畫解說, 產品廣告, 紀錄 Vlog, 新聞資訊, 品牌企業]
pace: [快, 中]
pairs_with: [FX-058, FX-061, FX-010, FX-081]
source: "synth: tools/sfx.py"
license: "自製合成，無版權限制，可商用"
learned: 2026-09-29
used_in: []
status: active
---

## 聲效
相機快門（Camera shutter），0.30 秒，擬音類。

## 幾時用
- 相片插入、出相、定格、海報框出現。

## 幾時唔好用
- 冇相片畫面時唔好用。

## 用法
- 建議音量 `volume: 0.45`（原聲保持 1.0，聲效喺人聲底下，唔好搶字）。
- 落聲時間：對準畫面動作嘅接觸格／出現格，唔係對準句子開頭。
- 混音：`python3 tools/sfx.py mix <source.mp4> <cues.json> <out.m4a>`，詳見 `lessons/sound-mixing.md`。
