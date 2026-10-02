---
id: healthy-days
name: Healthy Days（1分鐘醫聊室）
---
## 用喺
Healthy Days 出品、「1分鐘醫聊室」系列醫生片（例如江振昌醫生、袁孟豪醫生）。

## 常駐元素
- **右上角 logo 全片常駐**：`brands/healthy-days/logo_1min.png`，闊 278px，位置 x 742–1020、y 228–360（喺 IG 安全區內），z-index 最高（全屏卡／圖片都要見到）。
- **醫生名牌**：用 `brands/healthy-days/nametag_frame_wide.png`（由參考圖擦字，膠囊位置啱）（聽筒＋對話框樣板，空白版），上面一行專科（teal #13b8d0），下面一行姓名（藍 #1a80d0），字體用 Huninn（jf 粉圓）。例子見 `nametag_example.png`。**片頭出**（開場戲劇位之後即出，約 3.9–7.2 秒）。**大細跟以前片**：闊 370px、置中 x 355–725、y 965–1143；專科字 Huninn 34px（描邊 1.4px）、姓名 72px（描邊 2.7px）。呢個係品牌樣板尺寸，唔跟一般 64px 最細字規則。
- **Title tag**：藍 bar #2f68a8 由畫面左邊伸出，右邊圓角，最前面一個白色十字，白色粗黑體 64px（參考 `titletag_ref.png`）。用喺全屏圖片／資訊卡嘅標題，放左上 y 228。而家係動態系統嘅主角元素（#hero）T 狀態，同頂部關鍵詞係同一個元素變形。

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
- 頂部關鍵詞**置中 540、y 392**（logo 下面），全片 ≤ 4 個。
- Title tag 右邊唔好超過 x 720（logo 由 742 開始）。

## 風格包（2026-10-01 起）
- **預設用 `styles/kallaway` 淺色版**（用戶揀；深色版太暗黑）：`brands/healthy-days/tokens-kallaway.css` = 淡藍白底 #F2F7FC、深海軍藍字 #0B2A3A、logo 藍 #1A80D0 做重點、白色毛玻璃卡、淡藍光由下升起。深色後備：`tokens-kallaway-dark.css`（`--brand healthy-days:dark`）。
- 品牌固定元素照舊疊喺上面：右上 logo、名牌樣板、FX-051 方框字幕、title tag（全屏圖片標題）。
- 舊「藍膠囊」動態系統卡（`brands/healthy-days/motion-system.md`）已停用，只作歷史參考（doctor2 v5 用過）。

## 開場要戲劇化、緊張（只限 Healthy Days，用戶 2026-09-30）
- 0 秒特寫（#camInner 1.35–1.4，transform-origin 540px 420px）+ 暗角（clip，z-index ≥ 5）。
- 0.05 秒紅色心電圖線掃過；大字跟醫生講嗰個字撞入（scale 1.7→1，0.22 秒）+ 紅閃 + 確定性小震動。
- 聲效：心跳（0 秒）+ 低頻重擊（撞入落地）；拉返闊鏡時 whoosh，暗角淡走；之後名牌即出。

## 圖片風格（2026-10-02 用戶批：「可愛器官角色，啞面搪膠 3D」）
- 用戶參考：寫實口腔入面有眼有手嘅牙仔角色。試過寫實濕潤版 → 用戶話「太質感太真實有點噁心」→ 改啞面乾淨版，用戶批。
- **固定提示詞開頭（每張都用）**：`Cute stylized 3D character illustration, Pixar-style, soft matte smooth surfaces like a vinyl toy, clean and friendly, not realistic, no wet or glossy tissue, no veins, no gore.`
- **主角**：`A cute anthropomorphic heart character: round coral-pink heart-shaped body, big round brown eyes, tiny arms and legs.`（其他器官同樣寫法：形狀＋顏色＋big round eyes, tiny arms and legs）
- **固定結尾**：`Background: clean pale pink and soft light blue, gentle soft studio lighting, soft shadows, clean empty space at the top. Vertical composition, subject in the middle third. No text, no letters, no logos.`
- Canva `generate-image`，`PORTRAIT_9_16`。儀器畫面留白（no numbers）；藥物用通用形狀（no brand, no packaging）。
- 唔好用：寫實人體組織、濕潤反光、血管紋理；舊嘅黏土長者公仔同深藍光面心臟（doctor2 v5）已停用。

## 畫面比例同圖片版面（2026-10-02 用戶指示）
- 全片大約 **40% 見人物、40% 全屏（圖片為主，資訊卡最多 2 張）、20% 人物加圖片**。
- **跳鏡（轉機位、全屏入場退場）盡量喺句與句之間**，長句可以喺逗號位。
- 三款自家圖片卡（Kallaway 冇圖片卡）：`kallaway.x.image.full`（全屏圖 + 品牌標題條，膠囊放頂部留白位）、`kallaway.x.image.split`（上圖下人；主檔 #camInner scale 1.1、y 430）、`kallaway.x.image.pip`（胸口位浮框 + 膠囊，要用闊鏡 1.0）。
- 清單卡 `kallaway.t1.overview.checklist` 可以每行配圓形縮圖（slot p1–p4）。

## 版面規則（2026-10-02 用戶睇完節拍表同草稿之後定，取代上面舊位置）
- **效果唔好貼人面**：頭頂位（y 372–560）唔放關鍵詞／卡，只留 logo。疊喺講者嘅卡（關鍵詞、警號、劃線、圖片框）一律放胸口／字幕位：top ≥ 980（關鍵詞 1120、圖片框 900 配闊鏡 1.0）。
- **名牌放右下角**（left 640、top 1180），唔好放下巴／胸口正中。
- **開場**：大字 top 940；心電圖線壓扁（高 110）放 top 1272，喺大字同字幕之間，唔好橫過頸，亦唔好畀字幕遮住。
- **效果字唔細過字幕**：所有效果字 ≥ 76px（字幕 76px）；大字 110–120px；長過 7 字自動縮但唔細過 84px。
- **效果字已交代嗰句，字幕就唔出**（節拍表每拍寫 `skipcaps`）。醫療限定詞（有機會、可能、可以）要留喺效果字入面。
- **左上藍色標題條只做段落標題／分題**（例如「伴隨症狀」「有些長者」），84px；內容字用圖片頂部白底大字（big）或者藍色膠囊（tags）。連續兩張圖同一個分題：第二張 cue 寫 0（唔再滑入）。
- **圖片框（pip）入面張圖固定唔郁**；全屏圖同上圖下人先做慢推。
- **節拍表每格要列聲效**（幾秒、邊個聲、對住咩動作）。

## 鏡頭（2026-10-02 用戶睇草稿之後定）
- 跳鏡（轉機位、全屏入場退場）喺句與句之間，長句可以喺逗號位。
- **人物接人物唔好硬切放大／縮細**（1.0↔1.3 直接切似跳鏡）：用約 0.7 秒平滑推／拉（CAM 表 s0 寫 None）。由全屏圖片／資訊卡返嚟講者先直接切。
- 上圖下人：`#camInner` scale 1.1、y 430。圖片框：闊鏡 1.0。

## 用過嘅片
- doctor2 風格包版（江振昌醫生，氣喘同心臟退化，80.3 秒）：`storyboards/doctor2-k-beats.json`，13 張圖喺 `Video editing/doctor2/_work/d2k/img/`，草稿 `output/doctor2_k_draft2.mp4`（用戶 2026-10-02 批）。

## 2026-10-02 黎青龍護肝篇：用戶睇完節拍表第 1 版之後定
- **唔好自行加片尾聲明**（「以上內容只供參考」）或者任何用戶冇講嘅收尾卡；要加先問。
- **心電圖線只用喺心臟題材**。其他題材（肝、腎、腦…）開場只留特寫＋暗角，唔好加唔對題嘅圖形。
- **主角有大反應（笑、嬲、講笑、金句）就影返佢**：揀全屏圖位置之前，先逐段抽格睇表情；大反應位用淨人物或者胸口浮框（pip，唔加膠囊，字幕照出），全屏圖遲啲入／早啲走。
- **問題卡全片統一**：訪問片每條問題都用 `kallaway.x.question`，第一條都一樣，唔好用開場大字代替。
- **裁圖要睇主體**：上圖下人／浮框裁圖之後截圖檢查，主角同佢手上嘅嘢都要喺框入面（用 pos 調）。
- 浮框（pip）嘅膠囊同字幕同一個位：有字幕要出就唔好加膠囊。
