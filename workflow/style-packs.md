# 用風格包卡（9:16 用到先改）

## 卡嘅種類（新手包分類）
- **tier1 全屏**（蓋住講者）：`section` 章節／標題、`stat` 大數字、`overview` 清單／步驟／對比、`quote`、`thesis`。
- **tier2 支援**（講者保留）：`label` 關鍵詞／註解、`lower-third` 名牌／話題條、`list`、`equation`、`definition`。

## 揀卡
```
python3 tools/cards.py list --style kallaway --tier tier1 --purpose stat     # 全部
python3 tools/cards.py list --style kallaway --portrait                       # 已有 9:16 版
python3 tools/cards.py show kallaway.t1.overview.checklist                    # slots、時長
```
效果目錄網頁「教學包參考頁」可以睇每張卡截圖。同一條片同一 purpose 盡量用同一張卡（風格統一），唔同 purpose 先換卡。

## 改 9:16（未有直向版先做；改好永久入庫）
1. `python3 tools/cards.py adapt <id>` → `styles/<style>/cards-9x16/<id>.html`（已改 1080×1920 尺寸，版面未改）。
2. 人手改：
   - **版面**：直向單欄；字放喺 y 380–1556（頂 212 以上同 logo x742–1020 y228–360 唔放）；左右 ≥ 84px。
   - **tier2 唔遮面**：關鍵詞類放 logo 下面（y 380 起，底 ≤ 560），名牌類放下半（字幕區 y 1390–1520 要避開）。
   - **字級**：標題 ≥ 96px、內文 ≥ 64px；中文唔收窄字距；`white-space: nowrap` 防止斷字。
   - **時間**：根元素讀 `data-dur`（出場）同 `data-cues`（逐項出現秒數），冇就用預設；加平滑出場（縮細＋模糊，0.4–0.5 秒）。
   - **顏色**：寫死嘅 `rgba(55,189,248,…)` 改 `rgba(var(--accent-rgb),…)`；JS 入面要用色就 `getComputedStyle(ROOT).getPropertyValue('--accent-rgb')`。
   - **HyperFrames**：唔用 template literal（反引號）；資產路徑 `assets/…`；多詞標題用「｜」分詞組、`*重點*` 標重點（參考 `kallaway.t1.section.ascend`）。
   - 空 slot 自動隱藏（參考 checklist 嘅 i4）。
3. 預覽：砌一個 15 秒測試專案（講者片段 + logo + 卡），`npx hyperframes snapshot --at …` 自己先睇，再 render draft 俾用戶。
4. 用戶批咗：`python3 tools/cards.py verify <id> --note "doctor2 用過；title ≤ 8 字"`。

## 主題（淺／深）
- 品牌檔可以有兩個版本：`brands/<brand>/tokens-<style>.css`（預設）同 `tokens-<style>-dark.css`。Healthy Days 預設**淺色**（用戶 2026-10-01：深色太暗黑），`--brand healthy-days:dark` 用深色。
- 卡入面唔好寫死白色字：標題用 `var(--head)`、漸變大字起點 `var(--grad-start)`、大字光暈 `var(--kw-glow)`／`var(--kw-glow-peak)`、玻璃高光 `var(--glass-hi)`，淺深主題自動切換。

## 放入片
```
python3 tools/cards.py use kallaway.t2.label.keyword --project ~/hf/<proj> --name beat03 --dur 4 \
  --slots '{"term":"盡早檢查"}' --cues 0.6 --brand healthy-days
```
- 輸出 `compositions/beat03.html`（tokens＋品牌色內嵌、slot 已填、時長已設）同掛載 snippet（有 `data-composition-id`，填 START、TRACK）。
- cues 由 chars.json：`講嗰個字開始秒數 − 卡開始秒數`。
- 同一張卡可以用幾次（每次唔同 `--name`）。

## 已有 9:16 版（試做，待用戶批）
`kallaway.t2.label.keyword`、`kallaway.t1.overview.checklist`、`kallaway.t1.section.ascend`（doctor2 試做，2026-10-01；預覽 `Video editing/doctor2/output/kallaway_pilot.mp4`）。
