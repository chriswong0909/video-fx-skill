---
id: SFX-016
name: 閃光
name_en: Sparkle
category: accent
duration: 1.20
volume: 0.3
mood: [溫暖生活, 活潑年輕]
video_types: [口播知識, 訪問對談, 醫療健康, 動畫解說, 產品廣告, 紀錄 Vlog, 新聞資訊, 品牌企業]
pace: [中, 慢]
pairs_with: [FX-063, FX-027, FX-049, FX-042, FX-077]
source: "synth: tools/sfx.py"
license: "自製合成，無版權限制，可商用"
learned: 2026-09-29
used_in: []
status: active
---

## 聲效
閃光（Sparkle），1.20 秒，點綴類。

## 幾時用
- 發光字、光束、Logo 結尾、線稿變彩色。

## 幾時唔好用
- 醫療嚴肅題材少用。

## 用法
- 建議音量 `volume: 0.3`（原聲保持 1.0，聲效喺人聲底下，唔好搶字）。
- 落聲時間：對準畫面動作嘅接觸格／出現格，唔係對準句子開頭。
- 混音：`python3 tools/sfx.py mix <source.mp4> <cues.json> <out.m4a>`，詳見 `lessons/sound-mixing.md`。
