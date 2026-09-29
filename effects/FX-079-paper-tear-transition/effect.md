---
id: FX-079
name: 撕紙轉場
name_en: paper-tear-transition
category: transition
tags: [paper, tear, transition, reveal]
mood: [handmade, editorial, dramatic]
fits: [news, commentary, storytelling]
video_types: [新聞資訊, 口播知識, 紀錄 Vlog]
pace: [中, 快]
pairs_with: [FX-078, FX-081, FX-074]
conflicts_with: []
needs: [torn-edge-mask]
brand_color_ready: false
source: ref18-hk-retire-mgmtfee 0:26–0:28
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: "冇文字。"
placement: free
aspect: "16:9"
difficulty: medium
---

## 效果
上一個畫面（通常係剪報紙）好似被人由中間撕開：一條不規則毛邊裂口橫住打開，上下兩半各自向外飛走，露出下面嘅新畫面；裂口邊有白色紙纖維同陰影。

## 幾時用
由引用資料切返去實景／講者；段落之間需要一個有手作感嘅轉場。

## 幾時唔好用
極簡、科技感風格嘅片（質感唔夾）；太頻密（每條片 1–2 次夠）。

## 參數同節奏
- 上下兩半用同一條鋸齒 SVG path 做 clip-path（上半用 path 以上、下半用 path 以下）
- 毛邊：path 兩旁加 3px 白邊 + 陰影 0 6px 12px rgba(0,0,0,.45)
- 動畫：0.15s 微震（±3px），之後上半 y -60% rotate -3°、下半 y +60% rotate 2°，0.6s power2.in

## 實作重點
裂口 path 預先生成（隨機鋸齒），上下兩個 layer 各自複製舊畫面；新畫面喺下面。要做成 clip。

## 已知限制
舊畫面要係靜態（截圖／定格）先易做；動態片要兩個 video 同步。
