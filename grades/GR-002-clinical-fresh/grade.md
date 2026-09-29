---
id: GR-002
name: 醫療清新
name_en: clinical-fresh
video_types: [醫療健康, 口播知識, 品牌企業]
default_for: []
mood_zh: [專業醫療]
filters: "curves=master='0/0.02 0.5/0.52 0.85/0.9 1/1':r='0/0 0.5/0.485 1/0.99':b='0/0.01 0.5/0.52 1/1',eq=saturation=0.95"
source: original
learned: 2026-09-29
used_in: []
status: active
---

## 調色
偏白偏淨、光位微冷、整體明亮，似診所、藥廠廣告；膚色保留，背景白牆更白。

## 幾時用
診所環境、白色背景、藍色品牌（醫院、藥廠）；健康資訊片。

## 幾時唔好用
暖色木系環境（會變灰冷）；想溫暖親切嘅家庭醫生形象。

## 用法
- `python3 tools/grade.py apply source.mp4 GR-002 graded.mp4`（先自動校正白平衡同黑白位，再套風格；`--strength 0.6` 減弱；`--no-fix` 唔校正）
- 分鏡關卡用 `python3 tools/grade.py compare source.mp4 grade-compare.jpg GR-002 …` 出對比圖俾使用者揀。
- 膚色一定要人眼確認；醫療畫面（皮膚、傷口）用 `--strength 0.5` 或 GR-006。
