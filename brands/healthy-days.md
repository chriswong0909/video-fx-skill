---
id: healthy-days
name: Healthy Days（1分鐘醫聊室）
---
## 用喺
Healthy Days 出品、「1分鐘醫聊室」系列醫生片（例如江振昌醫生、袁孟豪醫生）。

## 常駐元素
- **右上角 logo 全片常駐**：`brands/healthy-days/logo_1min.png`，闊 278px，位置 x 742–1020、y 228–360（喺 IG 安全區內），z-index 最高（全屏卡／圖片都要見到）。
- **醫生名牌**：用 `brands/healthy-days/nametag_frame_wide.png`（由參考圖擦字，膠囊位置啱）（聽筒＋對話框樣板，空白版），上面一行專科（teal #13b8d0），下面一行姓名（藍 #1a80d0），字體用 Huninn（jf 粉圓）。例子見 `nametag_example.png`。**片頭出**（開場戲劇位之後即出，約 3.9–7.2 秒）。**大細跟以前片**：闊 370px、置中 x 355–725、y 965–1143；專科字 Huninn 34px（描邊 1.4px）、姓名 72px（描邊 2.7px）。呢個係品牌樣板尺寸，唔跟一般 64px 最細字規則。
- **Title tag**：藍 bar #2f68a8 由畫面左邊伸出，右邊圓角，最前面一個白色十字，白色粗黑體 64px（參考 `titletag_ref.png`）。用喺全屏圖片／資訊卡嘅標題，放左上 y 228。

## 字體
- **唔用襯線／尖角字（明體、Noto Serif TC）**。
- 名牌：Huninn（Google Fonts，jf open 粉圓）。
- 標題關鍵詞、字幕、標籤：Noto Sans TC 900。
- 全片最多兩款：Huninn + Noto Sans TC。

## 顏色
- logo 藍 #1a80d0、teal #13b8d0、橙 #ffb547（只喺 logo）、title tag 藍 #2f68a8
- 字幕底 #0b6f99（白字）
- 警示紅 #e8452c、正面綠 #1f9d6b（跟 SP-001 色彩意思）

## 版面（避開 logo）
- 頂部關鍵詞改為**左對齊** x 60 起，最闊 660px（≤5 字 @128px），唔好置中（會撞 logo）。

## 開場要戲劇化、緊張（只限 Healthy Days，用戶 2026-09-30）
- 0 秒特寫（#camInner 1.35–1.4，transform-origin 540px 420px）+ 暗角（clip，z-index ≥ 5）。
- 0.05 秒紅色心電圖線掃過；大字跟醫生講嗰個字撞入（scale 1.7→1，0.22 秒）+ 紅閃 + 確定性小震動。
- 聲效：心跳（0 秒）+ 低頻重擊（撞入落地）；拉返闊鏡時 whoosh，暗角淡走；之後名牌即出。
