# 多機位對色、抓鏡頭、防手震（tools/match.py）

2026-11-05 加。來源：Threads 一篇「11 個開源剪片 repo」整理。對比過我哋流程之後，只揀咗三個真係補到缺口嘅：
color-matcher、PySceneDetect、vid.stab。其餘（Auto-Editor、RIFE、Real-ESRGAN、Demucs、librosa）唔加入預設流程，原因見文末。

## 1. 多機位／多段對色（color-matcher）
**幾時用：** 闊鏡同近鏡分開兩部機、或者 Teleprompter 幾段分開錄，跳鏡時色溫、光暗唔同。
**次序：** 降噪 → 剪停頓 → **對色** → 白平衡校正（`color-grading.md`）→ `grade.py apply` 同一個 GR 預設。
```
python3 tools/match.py color near.mp4 wide.mp4 near_matched.mp4 --t 3 --rt 3 --strength 0.7
```
- 揀一部做「主機位」（通常闊鏡，或者光最靚嗰段），其他全部夾去佢。
- `--t`／`--rt` 揀兩邊**同一個姿勢、講者塊面清楚**嘅格；避開有手擋面、有字卡嘅格。
- 方法：MKL 由一格計出線性轉換 → 燒成 33 點 `.cube` → ffmpeg `lut3d` 套全片（快，唔使逐格跑 Python），`.cube` 留喺輸出旁邊可以重用。
- 預設 strength 0.7，留返少少原本質感；膚色變灰／變紅就降到 0.5。
- 出完用 `grade.py compare` 或者並排截圖睇跳鏡前後兩格，唔好淨係睇數字。

## 2. 參考片抓鏡頭（PySceneDetect）
**幾時用：** `workflow/reference-to-style.md` 第 1 步，補 `ref_style.py` 嘅剪接點。
```
python3 tools/match.py scenes ref.mp4 refs/<slug>/shots.json
```
輸出鏡頭數、平均／中位長度、每 10 秒剪幾多下同逐鏡時間。抽格睇動作時，揀每個鏡頭中間嗰格就唔會漏鏡。
淡入淡出、慢溶接可能抓唔到 → `--threshold 2` 再試；成條冇剪位會當一個鏡頭。

## 3. 防手震（vid.stab，FFmpeg 內置）
**幾時用：** 只限手持拍攝、睇得出搖。醫生腳架片**唔好跑**（會輕微縮放、白白損畫質）。
```
python3 tools/match.py stab in.mp4 in_stab.mp4 --shakiness 5 --smoothing 15
```
做喺剪停頓之前（成條原片一次過穩定，接位唔會跳）。邊位黑邊已經用 optzoom 自動放大遮走；放大太多（>8%）就降 smoothing。

## 唔加入預設流程嘅工具
| 工具 | 原因 |
|---|---|
| Auto-Editor | 只睇音量剪靜音；`cut.py` 識廣東話口頭禪、保護醫療限定詞，好過佢 |
| Demucs | DeepFilterNet 已處理背景噪；只有原片有背景音樂／旁人講嘢先考慮 |
| librosa | 預設冇 BGM；用戶俾 BGM 想剪位踩拍先用 |
| RIFE | 口播片同 MG 都唔使慢動作 |
| Real-ESRGAN | Canva 匯出已全尺寸；只有用戶俾低清截圖先考慮 |
| rembg、FFmpeg、HyperFrames | 已經喺流程入面 |
