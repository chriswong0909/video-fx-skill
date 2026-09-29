---
id: FX-049
name: 紙紋 Logo 結尾卡
name_en: paper-logo-endcard
category: transition
family: [SP-002]
tags: [end-card, logo, outro, brand]
mood: [calm, trustworthy]
fits: [medical, public-health, corporate, education]
video_types: [動畫解說, 品牌企業, 醫療健康]
pace: [中, 慢]
pairs_with: [FX-041]
conflicts_with: []
needs: [logo]
brand_color_ready: true
source: ref8-ha-heart-care 0:35.2–0:37.4
learned: 2026-09-29
used_in: []
status: active
cjk_fit: good
cjk_notes: 原片係中文（廣東話旁白），字體同排版可直接沿用。
difficulty: easy
---

## 效果
最後 3–4 秒：所有元素淡走，只剩紙紋背景，機構 logo 喺中間輕輕放大淡入並停留，最後淡出。

## 參數同節奏
- logo 寬度約畫面 18%；scale .92 → 1、opacity 0 → 1，0.6s power2.out
- 停留 2.5s；最後 0.4s 淡出（全片唯一可以做 exit 嘅位置）

## 實作重點
要用客戶提供嘅真實 logo 檔，唔可以自己畫或者用其他機構 logo。
