---
id: SFX-012
name: 上升張力
name_en: Short riser
category: riser
duration: 2.00
volume: 0.3
mood: [高級編輯感, 活潑年輕]
video_types: [口播知識, 訪問對談, 醫療健康, 動畫解說, 產品廣告, 紀錄 Vlog, 新聞資訊, 品牌企業]
pace: [快, 中]
pairs_with: [FX-006, FX-053, FX-063]
source: "synth: tools/sfx.py"
license: "自製合成，無版權限制，可商用"
learned: 2026-09-29
used_in: []
status: active
---

## 聲效
上升張力（Short riser），2.00 秒，張力類。

## 幾時用
- Hook 開場前、揭曉答案之前 2 秒；完結位接 impact 或 ding。

## 幾時唔好用
- 會蓋過人聲，只放喺講者停頓或開場。

## 用法
- 建議音量 `volume: 0.3`（原聲保持 1.0，聲效喺人聲底下，唔好搶字）。
- 落聲時間：對準畫面動作嘅接觸格／出現格，唔係對準句子開頭。
- 混音：`python3 tools/sfx.py mix <source.mp4> <cues.json> <out.m4a>`，詳見 `lessons/sound-mixing.md`。
