---
id: SFX-010
name: 錯誤警示聲
name_en: Error buzz
category: ding
duration: 0.50
volume: 0.3
mood: [活潑年輕, 專業醫療]
video_types: [口播知識, 訪問對談, 醫療健康, 動畫解說, 產品廣告, 紀錄 Vlog, 新聞資訊, 品牌企業]
pace: [快, 中]
pairs_with: [FX-047, FX-045, FX-013]
source: "synth: tools/sfx.py"
license: "自製合成，無版權限制，可商用"
learned: 2026-09-29
used_in: []
status: active
---

## 聲效
錯誤警示聲（Error buzz），0.50 秒，提示音類。

## 幾時用
- 打交叉、迷思、錯誤做法、警告橫額。

## 幾時唔好用
- 嚴肅病情（例如癌症）唔好用，會輕佻。

## 用法
- 建議音量 `volume: 0.3`（原聲保持 1.0，聲效喺人聲底下，唔好搶字）。
- 落聲時間：對準畫面動作嘅接觸格／出現格，唔係對準句子開頭。
- 混音：`python3 tools/sfx.py mix <source.mp4> <cues.json> <out.m4a>`，詳見 `lessons/sound-mixing.md`。
