# 廣東話轉錄

- 用 faster-whisper + `large-v3-turbo`（CT2 版：`deepdml/faster-whisper-large-v3-turbo-ct2`），`language="yue"`，`word_timestamps=True`。
  large-v3 int8 喺 4GB RAM 會 OOM；turbo 約 2.4GB，19 秒音頻 10 秒內完成。
- HF 下載用 `curl -C -` 續傳（單次指令有時限），下載完核對 content-length。
- Whisper 會將廣東話寫成書面語（是／這些／找）。**把握度低嘅字通常就係口語位**：係／呢啲／搵／啲。改成口語後必須叫使用者核對。
- 醫學詞要檢查同音錯字（例：心慮不正 → 心律不正）。
