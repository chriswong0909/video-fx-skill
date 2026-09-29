---
id: SFX-015
name: 心跳
name_en: Heartbeat
category: foley
duration: 1.80
volume: 0.5
mood: [專業醫療]
video_types: [口播知識, 訪問對談, 醫療健康, 動畫解說, 產品廣告, 紀錄 Vlog, 新聞資訊, 品牌企業]
pace: [中, 慢]
pairs_with: [FX-014, FX-050, FX-028]
source: "synth: tools/sfx.py"
license: "自製合成，無版權限制，可商用"
learned: 2026-09-29
used_in: []
status: active
---

## 聲效
心跳（Heartbeat），1.80 秒，擬音類。

## 幾時用
- 心臟、脈搏、緊張時刻、心電圖描繪。

## 幾時唔好用
- 唔好長時間 loop；手機喇叭要加大音量。

## 用法
- 建議音量 `volume: 0.5`（原聲保持 1.0，聲效喺人聲底下，唔好搶字）。
- 落聲時間：對準畫面動作嘅接觸格／出現格，唔係對準句子開頭。
- 混音：`python3 tools/sfx.py mix <source.mp4> <cues.json> <out.m4a>`，詳見 `lessons/sound-mixing.md`。
