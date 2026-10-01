# 模式 A：真人口播剪片（預設）
用喺：醫生片、講者對鏡頭講嘢。核心流程全部照行，另加：

1. **剪停頓**：`tools/cut.py`（`lessons/cutting-cantonese.md`），醫療限定詞永遠唔剪。
2. **字對聲**：`tools/words-template.py` 出 chars.json（改字表 FIX/DEL），所有字幕、特效時間由逐字時間計（`lessons/layout-safety.md` §9）。
3. **機位**：三機位 1.0／1.3／1.7，接位轉機位或 FX-040（`lessons/rhythm-variety.md`）。
4. **講者佔比**：≥ 60–70%；全屏卡／全屏圖由 treatment 定上限。
5. **風格包＋品牌**：`styles/<style>`（Healthy Days 預設 kallaway）+ `brands/<brand>.md`（logo 常駐、名牌、字幕）；卡由 `tools/cards.py use` 放入（`workflow/style-packs.md`），節拍跟 `workflow/beats.md`。
6. **聲效**：`sfx-events.json`（落地格）→ `tools/sfx_plan.py` → `tools/sfx.py mix`；冇 BGM。
