---
id: FX-044
name: 圓形插圖格逐個彈出
name_en: circle-icon-grid
category: list-chart
family: [SP-001, SP-002]
tags: [grid, icons, symptoms, numbered-list]
mood: [friendly, educational, clinical]
fits: [medical, education, public-health, explainer]
video_types: [動畫解說, 醫療健康]
pace: [中]
pairs_with: [FX-048, FX-050, FX-045]
conflicts_with: [FX-005]
needs: [illustration]
brand_color_ready: true
source: ref8-ha-heart-care 0:08.3–0:11.7
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: 原片係中文（廣東話旁白），字體同排版可直接沿用。
difficulty: easy
---

## 效果
2×2（或 2×3）格，每格一個圓形底色插圖（同一個角色做唔同動作／病徵），下面一個短標籤；跟住旁白逐格彈出，最後成個格一齊停留俾觀眾睇。

## 幾時用
列舉 3–6 個病徵、症狀、步驟，冇講者嘅解說片。

## 幾時唔好用
項目文字長（標籤最多 6 個中文字）。

## 參數同節奏
- 圓形 380px，底色 #f5b48a（暖橙）；標籤 44px 深啡 #4a3326 圓體粗字，白色描邊
- 每格：scale 0 → 1 back.out(1.6) 0.35s，標籤 0.15s 後由下升
- 間隔跟旁白（約 1–1.5 秒）

## 實作重點
角色插圖要同一人物一致（Higgsfield 用同一 reference 或 character sheet 生成）。
