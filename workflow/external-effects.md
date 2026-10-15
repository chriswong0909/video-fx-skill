# 外部效果配對（必做步驟；用戶 2026-10-15）

風格包（Kallaway／Vox）負責全片基礎設計（卡、字體、tokens）。**揀定風格包之後，一定要再睇外部效果來源**，替重點位揀 match 嘅效果，做成風格包嘅卡。
位置：Treatment 之後、節拍表之前（`skills/video-fx/SKILL.md` 第 5 節）。問卷第二輪「外部效果」選「今次唔使」先可以跳過（預設「照常配對」）。

## 1. 外部效果來源清單（之後會再加；加新來源喺呢度加一行，並寫明讀法）

| 來源 | 位置 | 讀法 |
|---|---|---|
| **text-motion-40**（40 款文字動畫） | 本機 `~/Documents/GitHub/text-motion-40/`；GitHub `chriswong0909/text-motion-40` | 先讀 `README.md` 使用規則，再用 `EFFECTS.md`（人睇）或 `effects.json`（程式讀）揀款；分格圖 `strips/`、單款短片 `clips/`。本機搵唔到就用 GitHub MCP 讀 `chriswong0909/text-motion-40`。查詢：`python3 tools/ext_effects.py list --use 數字`／`show 29` |

## 2. 配對流程
1. **列重點位**：由 Treatment 結構列出 hook、標題（章節）、關鍵詞、數字、轉場，每位寫原句同大約時間。
2. **按作用揀**：每個位去來源搵作用 match 嘅效果（text-motion-40 用 EFFECTS.md 嘅「用於」欄；例如數字 → 29 Odometer、公告／決定 → 03 Text Stamp、強調 → 38 Highlight Text），**每個位最多 2 個候選**。
3. **一定先開分格圖**：揀之前打開 `strips/<編號>_<名>.jpg`（8 格，每 0.75 秒一格，一次完整動作），需要時睇 `clips/` 短片。**EFFECTS.md 標 ⚠ 嘅款（01、02、17、18、20、33）冇睇分格圖唔准用**——只睇提示詞字體、比例、節奏會走樣。
4. **一條片外部效果以 2 至 3 款為主**，唔好太雜；同一作用用同一款（觀眾會認得）。
5. **出配對表俾用戶批**：欄位＝重點位｜原句｜候選效果（編號＋名）｜點解 match｜分格圖。寫 `matches.json`（格式見 `tools/ext_effects.py` 開頭），`python3 tools/ext_effects.py table matches.json out.html` 出頁（分格圖內嵌），用 Artifact 發佈，每輪改完用同一連結更新。**批咗先入節拍表。**
6. **全部唔適合**：可以一款都唔用，但配對表照出（列睇過邊啲、點解唔用），並喺 Treatment「外部效果」欄寫明。唔好硬用。

## 3. 用效果時嘅規則
- **動作同版式照參考**：字體粗幼、字嘅大細比例、入場方式、節奏，優先照分格圖做；可以因應 project 風格作修改，改咗要喺配對表／節拍表寫低改咗乜。
- **顏色轉做今次 project 嘅品牌色，唔好照抄參考顏色**：先睇參考用色嘅角色（底色、主字色、強調色），再逐個換做品牌色入面對應嘅顏色。**品牌色以每次 project 提供嘅為準**（`brands/<brand>.md`／`tokens-<style>.css`，未提供就問用戶）。換完檢查字同底色對比（文字同底色對比度 ≥ 4.5:1），手機細畫面都要睇得清。
- **做成卡時跟風格包規範**：`cards.py adapt <風格包相近嘅卡>` 做起點，套風格包 tokens，守 IG 安全區（左右 52、頂 212、底 1556 以外唔放字）同字級規則（效果字 ≥ 76px，大字 110–120px），**效果唔好貼人面**（疊喺講者嘅卡放胸口／字幕位 top ≥ 980）；左上標題條只做段落標題。
- **做完對比**：用 `npx hyperframes snapshot --at …` 每 0.75 秒截一格（共 8 格），同分格圖並排對比動作，唔啱就改，改完先交節拍表。
- **入庫**：用戶批咗嘅效果卡照常 `cards.py verify <id> --note "…" --source "text-motion-40#29"`；`styles/<style>/portrait.json` 該卡會記 `"source": "text-motion-40#29"`（編號係 text-motion-40 嘅編號），下次同作用位優先用已入庫嘅卡。
- **節拍表**：每拍加欄「外部效果」，寫用咗邊款（例如 `text-motion-40 #29 Odometer`）或「冇」；`beats.json` 對應欄位 `ext`。
- 來源只供個人參考學習（text-motion-40 README），唔好再發佈原片；片入面只用自己用 HTML／GSAP 重做嘅版本。
