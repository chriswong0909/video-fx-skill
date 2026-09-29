---
id: SFX-018
name: 低頻下沉
name_en: Sub drop
category: impact
duration: 1.20
volume: 0.45
mood: [高級編輯感]
video_types: [口播知識, 訪問對談, 醫療健康, 動畫解說, 產品廣告, 紀錄 Vlog, 新聞資訊, 品牌企業]
pace: [快, 中]
pairs_with: [FX-006, FX-053, FX-017]
source: "synth: tools/sfx.py"
license: "自製合成，無版權限制，可商用"
learned: 2026-09-29
used_in: []
status: active
---

## 聲效
低頻下沉（Sub drop），1.20 秒，重擊類。

## 幾時用
- 揭曉、轉入重要段落；可以同 riser 或 suck-in 接住用。

## 幾時唔好用
- 手機喇叭幾乎聽唔到，要配畫面動作。

## 用法
- 建議音量 `volume: 0.45`（原聲保持 1.0，聲效喺人聲底下，唔好搶字）。
- 落聲時間：對準畫面動作嘅接觸格／出現格，唔係對準句子開頭。
- 混音：`python3 tools/sfx.py mix <source.mp4> <cues.json> <out.m4a>`，詳見 `lessons/sound-mixing.md`。
