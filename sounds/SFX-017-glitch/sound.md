---
id: SFX-017
name: 故障雜訊
name_en: Glitch burst
category: accent
duration: 0.40
volume: 0.3
mood: [活潑年輕, 高級編輯感]
video_types: [口播知識, 訪問對談, 醫療健康, 動畫解說, 產品廣告, 紀錄 Vlog, 新聞資訊, 品牌企業]
pace: [快]
pairs_with: [FX-054, FX-075]
source: "synth: tools/sfx.py"
license: "自製合成，無版權限制，可商用"
learned: 2026-09-29
used_in: []
status: active
---

## 聲效
故障雜訊（Glitch burst），0.40 秒，點綴類。

## 幾時用
- RGB 分離、故障字；對準畫面閃爍幀。

## 幾時唔好用
- 溫暖／醫療片唔適合。

## 用法
- 建議音量 `volume: 0.3`（原聲保持 1.0，聲效喺人聲底下，唔好搶字）。
- 落聲時間：對準畫面動作嘅接觸格／出現格，唔係對準句子開頭。
- 混音：`python3 tools/sfx.py mix <source.mp4> <cues.json> <out.m4a>`，詳見 `lessons/sound-mixing.md`。
