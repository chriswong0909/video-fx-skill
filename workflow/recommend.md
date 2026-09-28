# 冇參考片時點揀效果

1. 讀 `registry.json`。
2. 按內容類型篩 `fits`（例如 talking-head、medical、product、podcast-clip、education）。
3. 按使用者想要嘅情緒篩 `mood`（warm / clinical / editorial / energetic / premium / playful）。
4. 覆蓋規則：
   - 必須：1 × hook、1 × caption、1 × camera
   - 15 秒以上：加 1 × cutaway 或 list-chart
   - 有列舉內容（1、2、3…）：用 list-chart
   - 有品牌色：用 caption 類中 `brand_color_ready: true` 嘅效果
5. 檢查 `pairs_with`（優先）同 `conflicts_with`（避免）。
6. 出 2 套方案（例如「暖色 podcast 風」vs「清爽醫療風」），列 FX-id 同預覽圖路徑，俾使用者揀。
