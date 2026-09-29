# 分鏡先行（慳 token 流程）

## 四個關卡（每關都要使用者確認先過）
1. **分鏡**：只用文字 + 效果庫預覽圖，唔渲染、唔生成。
2. **素材**：列出要生成嘅素材同 credits（Higgsfield `get_cost:true` 預先計），確認先生成。
3. **草稿**：`--quality draft` 渲染一次，只睇一張細 contact sheet（每格 ≤ 300px）。
4. **正式版**：`--quality high` 出片 + 換原音軌 + 核對。

## 分鏡點做
1. 轉錄（ASR）→ 按句切鏡頭（每鏡 1–4 秒）。
2. 每鏡填：時間、講緊咩、畫面描述、FX-id、素材（來源 code / higgsfield / canva / client / footage）、生成描述、credits；要聲效就加 `sfx`（`[{"sfx":"SFX-001","t":3.8}]`，t 係全片秒數，由 registry.json 嘅 sounds 按 pairs_with 揀）。分鏡網頁可以直接撳嚟試聽。
3. 寫入 `storyboards/<project>.json`（格式見 `_example.json`）。
4. `node scripts/build-storyboard.mjs storyboards/<project>.json` → `.html`。
5. 將 html stage 去雲端，用 Artifact 發佈（每個專案一條連結，修改就重新發佈同一條）。

## 慳 token 規則
- 分鏡階段唔好 Read 大圖；效果預覽已經喺 HTML 入面。
- 參考片分析只睇一張 contact sheet（fps 2、每格 225px）。
- 草稿只渲染一次；有問題改代碼後只重渲染出問題嗰段（切細 composition 或者用較短 data-duration 測試）。
- 唔好反覆截圖檢查；每個關卡最多睇一次。
- 使用者改分鏡只改 JSON，再 build，唔好重寫整份。
