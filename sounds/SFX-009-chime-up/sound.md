---
id: SFX-009
name: 上升提示音
name_en: Positive chime
category: ding
duration: 1.10
volume: 0.3
mood: [溫暖生活, 活潑年輕]
video_types: [口播知識, 訪問對談, 醫療健康, 動畫解說, 產品廣告, 紀錄 Vlog, 新聞資訊, 品牌企業]
pace: [中, 慢]
pairs_with: [FX-044, FX-057, FX-034]
source: "synth: tools/sfx.py"
license: "自製合成，無版權限制，可商用"
learned: 2026-09-29
used_in: []
status: active
---

## 聲效
上升提示音（Positive chime），1.10 秒，提示音類。

## 幾時用
- 正確答案、建議做法、正面結果、增長曲線。

## 幾時唔好用
- 同錯誤聲一齊用做「錯 vs 啱」對比最有效。

## 用法
- 建議音量 `volume: 0.3`（原聲保持 1.0，聲效喺人聲底下，唔好搶字）。
- 落聲時間：對準畫面動作嘅接觸格／出現格，唔係對準句子開頭。
- 混音：`python3 tools/sfx.py mix <source.mp4> <cues.json> <out.m4a>`，詳見 `lessons/sound-mixing.md`。
