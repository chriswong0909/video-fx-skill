---
id: SFX-001
name: 柔和風聲轉場
name_en: Soft whoosh
category: whoosh
duration: 0.75
volume: 0.35
mood: [專業醫療, 溫暖生活, 高級編輯感]
video_types: [口播知識, 訪問對談, 醫療健康, 動畫解說, 產品廣告, 紀錄 Vlog, 新聞資訊, 品牌企業]
pace: [中, 慢]
pairs_with: [FX-040, FX-006, FX-046, FX-003, FX-071, FX-068]
source: "synth: tools/sfx.py"
license: "自製合成，無版權限制，可商用"
learned: 2026-09-29
used_in: []
status: active
---

## 聲效
柔和風聲轉場（Soft whoosh），0.75 秒，轉場風聲類。

## 幾時用
- 推鏡、全屏過場入場、畫面左右滑走。聲音中心對準動作最快嗰格（約 0.3 秒後）。

## 幾時唔好用
- 每 10 秒唔好多過一次；硬切唔使配。

## 用法
- 建議音量 `volume: 0.35`（原聲保持 1.0，聲效喺人聲底下，唔好搶字）。
- 落聲時間：對準畫面動作嘅接觸格／出現格，唔係對準句子開頭。
- 混音：`python3 tools/sfx.py mix <source.mp4> <cues.json> <out.m4a>`，詳見 `lessons/sound-mixing.md`。
