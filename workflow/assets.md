# 素材來源次序（取代 assets-higgsfield.md 嘅次序部分）

效果嘅 `needs` 有 photo／illustration／3d-icons／cutout／scene-image 時，按以下次序攞素材。
**唔好一開始就跳去代碼插圖**；參考效果係用真相、3D 或者寫實畫面，扁平插圖會差好遠。

1. **Canva**（第一選擇）
   - `mcp__Canva__generate-image`：文字生成圖片，9:16 用 `aspectRatio: PORTRAIT_9_16`；用 Canva 帳戶自己嘅 AI 額度，唔使 Higgsfield credits。
   - 用戶 Canva 入面已有嘅相、品牌素材（先問用戶有冇）。
   - 生成前列出張數同用途，問用戶確認（Canva 額度按用戶方案）。
2. **原片截圖**：原片入面有冇可用嘅真實畫面（例如背景道具、模型、產品、手部動作）？截出嚟做全屏物件、卡片圖或膠囊遮罩。
3. **Higgsfield**：`get_cost:true` 預計 credits，列總數確認先生成；credits 唔夠就跳過。
4. **有授權嘅圖庫**（例如 Pexels、Unsplash）：逐張記錄來源同授權。
5. **代碼插圖**（最後先用）：跌到呢一步要明確話俾用戶知，並講明效果會比參考扁平；唔可以靜靜雞降級。

## 規則
- 醫學、人體、病徵圖像（無論 Canva、AI 或圖庫）一律標明「需醫生審核」。
- 唔好生成真實可辨認人物、品牌藥物包裝或假數據圖表。
- 分鏡每鏡嘅素材欄寫明 source：canva／footage／higgsfield／stock／code。
- 素材關卡一定要列出：邊鏡用邊個來源、預計額度或 credits。

## Canva connector 限制（2026-09-29 實測）
- `generate-image` 生成成功後，connector 只俾 200px 縮圖（`get-generate-image-job`、`get-assets` 都係）；改縮圖網址尺寸會 403。
- **攞原圖（已驗證，唔使用戶登入）**：`separate-image-layers`（asset_id = 生成圖嘅 media id）→ 等 job 完成攞 design id → `export-design`（`{"type":"png","width":1200}`）→ 用返回嘅 export-download 網址 `curl` 落載（網址有時限，即刻下載）→ commit 去素材資料夾。1200×1200 夠全屏卡用。
- 下載前要用戶同意（一次過同意整批即可）；分層設計會留喺用戶 Canva 帳戶，可以之後喺 Canva 刪。
- 素材關卡問確認時就要講明呢一步，唔好生成完先發現。
