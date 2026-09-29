---
id: SFX-005
name: 柔和 pop
name_en: Soft pop
category: pop
duration: 0.14
volume: 0.45
mood: [專業醫療, 溫暖生活]
video_types: [口播知識, 訪問對談, 醫療健康, 動畫解說, 產品廣告, 紀錄 Vlog, 新聞資訊, 品牌企業]
pace: [中, 慢]
pairs_with: [FX-032, FX-067, FX-038, FX-064]
source: "synth: tools/sfx.py"
license: "自製合成，無版權限制，可商用"
learned: 2026-09-29
used_in: []
status: active
---

## 聲效
柔和 pop（Soft pop），0.14 秒，彈出類。

## 幾時用
- 清單逐項出、名牌出現；比泡泡聲穩重，適合醫療。

## 幾時唔好用
- 同一句入面唔好同泡泡聲混用。

## 用法
- 建議音量 `volume: 0.45`（原聲保持 1.0，聲效喺人聲底下，唔好搶字）。
- 落聲時間：對準畫面動作嘅接觸格／出現格，唔係對準句子開頭。
- 混音：`python3 tools/sfx.py mix <source.mp4> <cues.json> <out.m4a>`，詳見 `lessons/sound-mixing.md`。
