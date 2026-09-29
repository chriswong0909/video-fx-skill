---
id: GR-005
name: 明亮生活
name_en: bright-lifestyle
video_types: [紀錄 Vlog, 產品廣告, 口播知識]
default_for: [紀錄 Vlog]
mood_zh: [活潑年輕]
filters: "eq=brightness=0.03:gamma=1.06:saturation=1.12,curves=r='0/0 0.5/0.51 1/1':b='0/0 0.5/0.49 1/1'"
source: original
learned: 2026-09-29
used_in: []
status: active
---

## 調色
明亮、通透、色彩鮮但唔俗，略暖；似生活 vlog、年輕品牌。

## 幾時用
vlog、生活分享、活潑年輕嘅健康貼士。

## 幾時唔好用
嚴肅題材；原片已經過曝。

## 用法
- `python3 tools/grade.py apply source.mp4 GR-005 graded.mp4`（先自動校正白平衡同黑白位，再套風格；`--strength 0.6` 減弱；`--no-fix` 唔校正）
- 分鏡關卡用 `python3 tools/grade.py compare source.mp4 grade-compare.jpg GR-005 …` 出對比圖俾使用者揀。
- 膚色一定要人眼確認；醫療畫面（皮膚、傷口）用 `--strength 0.5` 或 GR-006。
