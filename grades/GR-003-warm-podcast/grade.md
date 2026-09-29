---
id: GR-003
name: 暖色 Podcast
name_en: warm-podcast
video_types: [訪問對談, 口播知識, 紀錄 Vlog]
default_for: []
mood_zh: [溫暖生活]
filters: "curves=master='0/0.06 0.5/0.5 1/0.95':r='0/0 0.5/0.53 1/1':b='0/0 0.5/0.46 1/0.96',eq=saturation=0.9,vignette=angle=PI/5"
source: original
learned: 2026-09-29
used_in: []
status: active
---

## 調色
桃杏暖色、黑位微提（啞光）、輕微降飽和、四角暗角；溫暖、似 podcast 同 lifestyle 訪問（同 FX-015 一致）。

## 幾時用
閒談訪問、分享經歷、溫情題材。

## 幾時唔好用
需要準確顏色（皮膚病、傷口、化驗）；冷色品牌。

## 用法
- `python3 tools/grade.py apply source.mp4 GR-003 graded.mp4`（先自動校正白平衡同黑白位，再套風格；`--strength 0.6` 減弱；`--no-fix` 唔校正）
- 分鏡關卡用 `python3 tools/grade.py compare source.mp4 grade-compare.jpg GR-003 …` 出對比圖俾使用者揀。
- 膚色一定要人眼確認；醫療畫面（皮膚、傷口）用 `--strength 0.5` 或 GR-006。
