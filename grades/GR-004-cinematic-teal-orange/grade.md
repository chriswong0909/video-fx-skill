---
id: GR-004
name: 電影青橙
name_en: cinematic-teal-orange
video_types: [產品廣告, 品牌企業, 紀錄 Vlog]
default_for: [產品廣告]
mood_zh: [高級編輯感]
filters: "curves=r='0/0 0.25/0.2 0.75/0.81 1/1':g='0/0 0.25/0.235 0.75/0.765 1/1':b='0/0.04 0.25/0.3 0.75/0.69 1/0.96',eq=saturation=1.06"
source: original
learned: 2026-09-29
used_in: []
status: active
---

## 調色
陰影偏青、光位（膚色）偏橙、對比較強，電影同廣告常見色調，畫面有質感。

## 幾時用
品牌片、產品廣告、形象片、有戶外或霓虹場景。

## 幾時唔好用
醫療專業講解（顏色唔中性）；本身已經好多藍綠嘅畫面（會過火）。

## 用法
- `python3 tools/grade.py apply source.mp4 GR-004 graded.mp4`（先自動校正白平衡同黑白位，再套風格；`--strength 0.6` 減弱；`--no-fix` 唔校正）
- 分鏡關卡用 `python3 tools/grade.py compare source.mp4 grade-compare.jpg GR-004 …` 出對比圖俾使用者揀。
- 膚色一定要人眼確認；醫療畫面（皮膚、傷口）用 `--strength 0.5` 或 GR-006。
