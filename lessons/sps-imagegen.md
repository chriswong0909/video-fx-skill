# 用 SPS（Social Page Studio）生影片素材圖（2026-11-03 脂肪肝篇，用戶批：以後用 SPS 生圖，唔使再問）

- Page `healthydays`、pillar **`ai-video-imagegen`**（Ai Video ImageGen）：專做影片 MG 素材，純白底、單一主體、冇字。
- 流程（每張圖）：`create_agent_draft_post`（sourceBasis creative_nonfactual）→ `submit_agent_authored_output`（outputType instagram／facebook，fields：headline、captionMarkdown、imagePrompt）→ `generate_images`（唔填 platform＝全部 output 一齊生）→ 約 1 分鐘後 `get_post_detail` 攞 `generatedMediaUrl` → curl。
  - 一個草稿帖可以有 instagram＋facebook 兩個 output＝兩張圖；carousel 唔支援 agent 寫入。
  - 輸出固定 4:5、1024×1280 PNG。
- 白底其實係 #FCFCFC（252）：唔好用 CSS `mix-blend-mode: multiply`（HyperFrames composition 入面無效，會見到白框）。用 numpy 以邊框中位色做白，`alpha = clip((白 − min通道 − 7) × 4.5)`，再反乘還原顏色，存 `_a.png`。
- 素材入 MG 一定要郁（跌落擠壓、原地跑、推、彈跳慶祝），配淡色主題背景同 #38 螢光筆大字；靜態去背圖仍然禁用。
- App 權限：「Always allow」係逐個工具計，SPS 每個新工具第一次用都會彈一次；同一條片盡量用同一組工具，減少彈窗。
- 範例：`workflow/examples/lai-liver/ep2/`（gen_subj.py、sfat／sstarch／srice／sjog／sheal.html）。
