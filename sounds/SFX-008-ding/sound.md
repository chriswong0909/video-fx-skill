---
id: SFX-008
name: 重點 ding
name_en: Highlight ding
category: ding
duration: 1.60
volume: 0.3
mood: [專業醫療, 溫暖生活]
video_types: [口播知識, 訪問對談, 醫療健康, 動畫解說, 產品廣告, 紀錄 Vlog, 新聞資訊, 品牌企業]
pace: [中, 慢]
pairs_with: [FX-065, FX-027, FX-022, FX-050]
source: "synth: tools/sfx.py"
license: "自製合成，無版權限制，可商用"
learned: 2026-09-29
used_in: []
status: active
---

## 聲效
重點 ding（Highlight ding），1.60 秒，提示音類。

## 幾時用
- 金句、重點字、圈註出現；一條片 1–3 次。

## 幾時唔好用
- 唔好每句都 ding，會變廉價。

## 用法
- 建議音量 `volume: 0.3`（原聲保持 1.0，聲效喺人聲底下，唔好搶字）。
- 落聲時間：對準畫面動作嘅接觸格／出現格，唔係對準句子開頭。
- 混音：`python3 tools/sfx.py mix <source.mp4> <cues.json> <out.m4a>`，詳見 `lessons/sound-mixing.md`。
