---
id: SFX-011
name: 低頻重擊
name_en: Low impact
category: impact
duration: 1.40
volume: 0.4
mood: [高級編輯感, 專業醫療]
video_types: [口播知識, 訪問對談, 醫療健康, 動畫解說, 產品廣告, 紀錄 Vlog, 新聞資訊, 品牌企業]
pace: [快, 中]
pairs_with: [FX-017, FX-053, FX-048, FX-062, FX-076]
source: "synth: tools/sfx.py"
license: "自製合成，無版權限制，可商用"
learned: 2026-09-29
used_in: []
status: active
---

## 聲效
低頻重擊（Low impact），1.40 秒，重擊類。

## 幾時用
- 大字砸落、章節標題、物件跌落著地嗰格。

## 幾時唔好用
- 手機喇叭聽唔到低頻，唔好靠佢做唯一提示。

## 用法
- 建議音量 `volume: 0.4`（原聲保持 1.0，聲效喺人聲底下，唔好搶字）。
- 落聲時間：對準畫面動作嘅接觸格／出現格，唔係對準句子開頭。
- 混音：`python3 tools/sfx.py mix <source.mp4> <cues.json> <out.m4a>`，詳見 `lessons/sound-mixing.md`。
