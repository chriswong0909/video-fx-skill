---
id: SFX-003
name: 反向吸入
name_en: Reverse suck-in
category: riser
duration: 0.90
volume: 0.35
mood: [高級編輯感, 活潑年輕]
video_types: [口播知識, 訪問對談, 醫療健康, 動畫解說, 產品廣告, 紀錄 Vlog, 新聞資訊, 品牌企業]
pace: [快, 中]
pairs_with: [FX-006, FX-017, FX-053, FX-063]
source: "synth: tools/sfx.py"
license: "自製合成，無版權限制，可商用"
learned: 2026-09-29
used_in: []
status: active
---

## 聲效
反向吸入（Reverse suck-in），0.90 秒，張力類。

## 幾時用
- 大字或全屏畫面出現之前 0.9 秒開始，完結一刻正正係畫面出現。

## 幾時唔好用
- 唔好連續用兩次；開場第一秒用就好。

## 用法
- 建議音量 `volume: 0.35`（原聲保持 1.0，聲效喺人聲底下，唔好搶字）。
- 落聲時間：對準畫面動作嘅接觸格／出現格，唔係對準句子開頭。
- 混音：`python3 tools/sfx.py mix <source.mp4> <cues.json> <out.m4a>`，詳見 `lessons/sound-mixing.md`。
