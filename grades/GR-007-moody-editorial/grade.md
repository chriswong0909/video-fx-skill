---
id: GR-007
name: 暗調編輯感
name_en: moody-editorial
video_types: [品牌企業, 訪問對談, 產品廣告]
default_for: []
mood_zh: [高級編輯感]
filters: "eq=brightness=-0.04:saturation=0.8,curves=master='0/0.06 0.3/0.25 0.7/0.7 1/0.93':b='0/0.04 0.4/0.42 1/0.98'"
source: original
learned: 2026-09-29
used_in: []
status: active
---

## 調色
偏暗、低飽和、黑位啞光、陰影微冷；雜誌式高級感，似 Apple、時裝訪問。

## 幾時用
高級品牌、人物專訪、設計感題材。

## 幾時唔好用
醫療衞教（太沉）；原片已經偏暗。

## 用法
- `python3 tools/grade.py apply source.mp4 GR-007 graded.mp4`（先自動校正白平衡同黑白位，再套風格；`--strength 0.6` 減弱；`--no-fix` 唔校正）
- 分鏡關卡用 `python3 tools/grade.py compare source.mp4 grade-compare.jpg GR-007 …` 出對比圖俾使用者揀。
- 膚色一定要人眼確認；醫療畫面（皮膚、傷口）用 `--strength 0.5` 或 GR-006。
