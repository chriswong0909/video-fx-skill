---
id: SFX-007
name: 打字聲
name_en: Typing ticks
category: ui
duration: 1.20
volume: 0.3
mood: [專業醫療, 新聞資訊]
video_types: [口播知識, 訪問對談, 醫療健康, 動畫解說, 產品廣告, 紀錄 Vlog, 新聞資訊, 品牌企業]
pace: [中, 慢]
pairs_with: [FX-066, FX-052, FX-059]
source: "synth: tools/sfx.py"
license: "自製合成，無版權限制，可商用"
learned: 2026-09-29
used_in: []
status: active
---

## 聲效
打字聲（Typing ticks），1.20 秒，介面類。

## 幾時用
- 逐字打出、數字逐位出；長度可以剪到同動畫一樣。

## 幾時唔好用
- 講者講緊重點時會搶聲，放喺停頓位。

## 用法
- 建議音量 `volume: 0.3`（原聲保持 1.0，聲效喺人聲底下，唔好搶字）。
- 落聲時間：對準畫面動作嘅接觸格／出現格，唔係對準句子開頭。
- 混音：`python3 tools/sfx.py mix <source.mp4> <cues.json> <out.m4a>`，詳見 `lessons/sound-mixing.md`。
