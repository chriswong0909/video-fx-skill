---
id: GR-006
name: 新聞中性
name_en: news-neutral
video_types: [新聞資訊, 動畫解說]
default_for: [新聞資訊, 動畫解說]
mood_zh: []
filters: "curves=master='0/0.01 0.5/0.5 1/0.99'"
source: original
learned: 2026-09-29
used_in: []
status: active
---

## 調色
只做校正（白平衡、黑白位）加極輕對比，盡量保持真實顏色；似新聞紀實。

## 幾時用
新聞、紀實、真實記錄；混合多個來源素材想統一。

## 幾時唔好用
想要明顯風格。

## 用法
- `python3 tools/grade.py apply source.mp4 GR-006 graded.mp4`（先自動校正白平衡同黑白位，再套風格；`--strength 0.6` 減弱；`--no-fix` 唔校正）
- 分鏡關卡用 `python3 tools/grade.py compare source.mp4 grade-compare.jpg GR-006 …` 出對比圖俾使用者揀。
- 膚色一定要人眼確認；醫療畫面（皮膚、傷口）用 `--strength 0.5` 或 GR-006。
