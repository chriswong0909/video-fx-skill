---
id: GR-001
name: 專業專訪
name_en: professional-interview
video_types: [醫療健康, 口播知識, 訪問對談, 品牌企業]
default_for: [醫療健康, 口播知識, 訪問對談, 品牌企業]
mood_zh: [專業醫療]
filters: "curves=master='0/0.01 0.25/0.235 0.75/0.77 1/0.99':r='0/0 0.75/0.765 1/1':b='0/0 0.75/0.74 1/1',eq=saturation=1.03"
source: original
learned: 2026-09-29
used_in: []
status: active
---

## 調色
乾淨中性、膚色自然略暖、輕微 S 曲線加少少立體感；似電視台專訪同醫院官方片。醫生口播預設用呢個。

## 幾時用
醫生、專家口播、訪問、機構片；想專業可信、唔搶戲。

## 幾時唔好用
想要強烈風格或情緒；室內燈光本身已經好靚、原色就啱。

## 用法
- `python3 tools/grade.py apply source.mp4 GR-001 graded.mp4`（先自動校正白平衡同黑白位，再套風格；`--strength 0.6` 減弱；`--no-fix` 唔校正）
- 分鏡關卡用 `python3 tools/grade.py compare source.mp4 grade-compare.jpg GR-001 …` 出對比圖俾使用者揀。
- 膚色一定要人眼確認；醫療畫面（皮膚、傷口）用 `--strength 0.5` 或 GR-006。
