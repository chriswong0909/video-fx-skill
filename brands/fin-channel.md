---
id: fin-channel
name: 財經頻道（#203699）
---
## 用喺
財經頻道短片，觀眾係 90 後投資者。第一條片：40S（兩人訪問「AI 會唔會取代老師」，2026-10-03）。

## 顏色（用戶 2026-10-04）
- **只用品牌色 #203699（深寶藍）同相配嘅顏色**：淺紫藍 #6E86E8、深海軍藍 #0E1A4D、白。**唔用橙色**，亦唔用顏色分角色（之前「藍＝AI、暖橙＝老師」已取消）。

## 風格包
- `styles/kallaway` 淺色版：`brands/fin-channel/tokens-kallaway.css`。
- **唔好混入 Healthy Days 風格元素**（左上標題條、實色膠囊、圓章問題卡、`kallaway.x.image.*`、`kallaway.x.question`）。用風格包原卡：
  問題卡 `kallaway.t2.label.qmark`、名牌 `kallaway.t2.lower-third.glasscard`、流程 `kallaway.t1.overview.flow`、清單 `kallaway.t1.overview.checklist`（兩張都可以加 img 做底）、關鍵詞 `kallaway.t2.label.keyword`。
- 圖片用 `kallaway.x.photo.full／split／frame`（只做圖片底，冇字），字用關鍵詞卡疊上去（overlay，z 16）。

## 常駐元素
- **未有 logo**（用戶未提供）；唔好自己加水印。
- **字幕**：光暈字幕 FX-039：白字 76px + **黑／深灰光暈**（唔用品牌色），top 1400，中英夾雜，口語照寫。

## 節奏同聲音
- 節奏密集、聲效密、冇 BGM。人聲 -16 LUFS。

## 畫面比例
- 目標 40% 人物／40% 全屏／20% 人物加圖片。

## 圖片風格（2026-10-03 用戶批）
- 寫實底加超現實、科幻、科技感，藍色調為主。Canva `generate-image`，9:16。（40S 圖 3、6、7 係暖橙光，用戶之後話唔要橙色，新圖唔好再用暖光。）

## 版面（闊鏡雙人訪問位）
- 兩人坐喺 y 600–1700，上面約四成係白牆：問題卡放白牆（top 300），離頭頂 ≥ 130px。
- 單人推近（1.45 倍）時白牆冇咗：問題卡落返胸口位，圖片框放講者旁邊。

## 用過嘅片
- 40S（39.3 秒）：`storyboards/40s-beats.json`。
