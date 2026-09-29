---
id: FX-029
name: UI 元件解說
name_en: ui-widget-explainer
category: list-chart
family: [SP-001]
tags: [ui, calendar, pill-button, chat-bubble, checklist]
mood: [clean, modern, clinical]
fits: [education, medical, lifestyle, product]
video_types: [醫療健康, 口播知識]
pace: [中]
pairs_with: [FX-028, FX-018, FX-033]
conflicts_with: []
needs: []
brand_color_ready: true
source: ref5-aging-routine 0:01.5–0:11、ref4-brain-explainer 0:10–0:12.5
learned: 2026-09-29
used_in: [doctor-stairs-breath]
status: active
cjk_fit: adjust
cjk_notes: "UI 字最少 64px；中文打字機每字約 0.06 秒。"
difficulty: medium
---

## 效果
將講者講嘅習慣／步驟變成手機 UI 元件：日曆逐日剔藍點、膠囊按鈕（圖示 + 文字打字機效果「Train 3 Times」）、物件上面彈出藍色對話泡標籤（Taking Cold Shower）、相片卡片……一個接一個喺淺灰藍背景上出現同推走，底部配單字字幕（FX-018 深色版）。

## 幾時用

講「每週做幾多次」「生活習慣清單」「療程步驟」；想要實用、易明嘅感覺。

## 參數同節奏


- 背景 linear-gradient(#e9eef5 → #c9d3e0)
- 卡片白色、圓角 22、陰影 0 20px 40px rgba(40,60,90,.18)
- 日曆：每剔一日 0.12s（藍圈 scale 0 → 1）
- 膠囊按鈕：淺藍底，文字逐字打出 0.04s／字
- 對話泡：藍 #1976f2 白字，彈出 back.out 0.3s
- 每項 1–2 秒，用滑走（x -300、blur）過渡


## 實作重點

全部用 HTML/CSS 元件，唔使素材；字幕改深色（#222）因為背景淺。
