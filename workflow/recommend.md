# 冇參考片時點揀效果

1. 讀 `registry.json`。
2. 先按 `video_types`（影片類型：口播知識／訪問對談／醫療健康／動畫解說／產品廣告／紀錄 Vlog／新聞資訊／品牌企業）同 `pace`（節奏：快／中／慢，對應問卷第二輪節奏答案）篩；再按內容類型篩 `fits`（例如 talking-head、medical、product、podcast-clip、education）。
3. 按使用者想要嘅情緒篩 `mood`（warm / clinical / editorial / energetic / premium / playful）。
4. 排除 `status: banned` 嘅效果；中文片優先 `cjk_fit: good`。
5. 覆蓋規則：
   - 必須：1 × hook、1 × caption、1 × camera
   - 15 秒以上：加 1 × cutaway 或 list-chart
   - 有列舉內容（1、2、3…）：用 list-chart
   - 有品牌色：用 caption 類中 `brand_color_ready: true` 嘅效果
5. 檢查 `pairs_with`（優先）同 `conflicts_with`（避免）。
6. 出 2 套方案（例如「暖色 podcast 風」vs「清爽醫療風」），列 FX-id 同預覽圖路徑，俾使用者揀。

## 按動態系統卡揀（2026-10-01）
1. 先睇系統卡准用邊幾款零件 → 只喺 registry 對應 `component` 揀。
2. `entry` 要喺系統卡入場文法入面；唔喺就要換皮（改入場方式）先用，或者唔用。
3. `style_bound: true` 嘅效果只喺佢 `family` 嘅預設用；Healthy Days 等品牌片預設唔揀。
4. composition `<head>` 依次貼：預設 `tokens.css` → 品牌 `brands/<brand>/tokens.css`（例如 Healthy Days）。效果會自動跟品牌色同節奏。
