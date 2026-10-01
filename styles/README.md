# 風格包（styles/）

來源：HyperFrames 新手包（hyperframes-student-kit，Nate Herk，MIT 授權，見 `LICENSE-hyperframes-student-kit.txt`）嘅 `style-library/`。
「Vox」「Kallaway」只係美學參考名，唔係官方品牌。新手包原本規則：`GUIDE-kit.md`；動態總綱：`MOTION_PHILOSOPHY.md`。

| 風格包 | 感覺 | 卡數 | 用喺 |
|---|---|---|---|
| `kallaway/` | 暗底、品牌色光暈由下升起、毛玻璃卡、發光大字、順滑 glide＋bloom | 300 | **Healthy Days 預設**、知識／醫療／科技 |
| `vox-explainer/` | 紙感、拼貼、襯線大字、手繪箭咀圈註、定格感 | 106 | 解說、歷史、新聞（品牌禁襯線就唔用） |

每個風格包：`DESIGN.md`（必讀，尤其「What NOT to do」）、`tokens.css`、`style.json`（全部卡：id、tier、purpose、slots、時長）、
`cards/`（16:9 原卡，唔好改）、`cards-9x16/`（直向中文版，用到先改）、`portrait.json`（邊張已有直向版、驗證咗未）、
`tokens-9x16.css`（直向字級＋中文字體）。品牌覆蓋：`brands/<brand>/tokens-<style>.css`。

工具：`python3 tools/cards.py list|show|adapt|use|verify`（見 `workflow/style-packs.md`）。
