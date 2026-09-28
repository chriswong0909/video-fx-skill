---
id: FX-011
name: 人像分層補光
name_en: matte-relight
category: grade-light
tags: [matting, relight, background-blur, depth]
mood: [clinical, premium, clean]
fits: [talking-head, medical, interview]
pairs_with: [FX-009, FX-012]
conflicts_with: [FX-015]
needs: [matting, python-onnxruntime]
brand_color_ready: true
source: original（doctor2-editorial）
learned: 2026-09-28
used_in: [doctor2-editorial]
difficulty: hard
---

## 效果
用人像摳圖（RVM）分開講者同背景：背景虛化、壓暗、降飽和；講者臉部加柔和主光、一邊輕微變暗做立體感、加淡輪廓光。效果似專業打光 + 淺景深。

## 幾時用
背景雜亂、平均打光、講者唔突出。

## 幾時唔好用
想保留環境真實感；講者大動作（摳圖邊位易出錯）。

## 參數同節奏
背景：飽和 0.72、亮度 0.74、暈影 0.62；主光 screen 0.08；輪廓光 0.10；對比 1.10。

## 實作重點
`tools/relight.py`，見 `lessons/relight.md`。19 秒約 3.5 分鐘（分兩段跑）。

## 已知限制
只係分層調色，改唔到光向同陰影；頭髮邊位放大睇有柔邊；前景枱會一齊虛化。
