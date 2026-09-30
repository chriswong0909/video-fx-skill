# 模式 C：無真人講解片（faceless explainer）
用喺：旁白 + 全動態或生成鏡頭（例如 Vox 式拼貼、白板、等距插畫）。

1. **稿**：先定稿（用戶俾或者一齊寫），分場（每場 3–8 秒），每場一句重點。
2. **旁白**：用戶錄音優先；要合成就用 Higgsfield `generate_audio`／`create_voice`（先報 credits）。旁白轉錄出 chars.json，畫面照字對聲。
3. **風格鎖定**：揀一個風格（參考片 style-guide 或 Higgsfield explainer preset 做起點，但要改到唔 generic），寫入動態系統卡；生成鏡頭全部用同一張風格參考圖（style reference）鎖定，第 40 鏡要同第 1 鏡一致。
4. **生成鏡頭**：Higgsfield `models_explore(action:'recommend')` 揀模型；prompt 描述**樣子同感覺**（「柔光斜掃過紙面」），唔寫軟件術語；結尾加「所有文字清晰完整、唔好模糊」。重要鏡頭一次出 3–6 個變體（其中一個出位啲）再揀。
5. **合成**：生成鏡頭做底，文字、箭嘴、數字、標籤一律喺 HyperFrames 用 code 疊（字唔好交俾生成模型畫）。
6. 其餘照核心：節拍表 + 關鍵格批核 → 草稿 → 正式版。
