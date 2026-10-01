---
id: FX-054
name: 故障 RGB 分離大字
name_en: glitch-rgb-text
category: transition
family: [SP-003]
tags: [glitch, rgb-split, big-type, dark]
mood: [dramatic, edgy, energetic]
fits: [finance, tech, talking-head, education]
video_types: [口播知識, 品牌企業]
pace: [快]
pairs_with: [FX-053, FX-052]
conflicts_with: []
needs: []
brand_color_ready: true
source: ref9-fire-investment 0:11–0:12、0:17–0:19
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: 粗黑體 2 個字最有力；筆畫密嘅字 glitch 後都仲認得。
placement: center
difficulty: medium
style_bound: true
bound_reason: "故障 RGB 分離色係效果本身"
component: headline
entry: [cut]
---

## 效果
全屏深色或模糊背景，一兩個超大字（辛苦、未計得清）出現時帶 RGB 色散同橫向撕裂抖動（故障效果），約 0.3 秒後穩定；可以配紅色字表示警告。

## 幾時用
負面情緒、痛點、「危機」位；一條片最多 2 次。

## 參數同節奏
- 字 220–260px Sans 900；三層：紅 (#ff2d55) x-6、青 (#18e0ff) x+6、白主層，mix-blend-mode: screen
- 抖動：0.3s 內 6 次隨機 x ±20、clip-path 橫條切片（seeded PRNG）
- 背景：原片 blur(20px) brightness(.4) 或黑底

## 實作重點
唔用 Math.random，用 seeded PRNG 預先生成抖動數值；做 clip。
