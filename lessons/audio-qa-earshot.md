# 聲音 QA：用 Earshot「聽」成品

我哋聽唔到聲，所以出片前用 [Earshot](https://github.com/Leonxlnx/earshot)（MIT、CPU、模型約 1.4 GB）做一次「聽」：佢講到量度，唔講到品味。

## 點用
- 安裝：`pip install torch --index-url https://download.pytorch.org/whl/cpu`，再 `pip install git+https://github.com/Leonxlnx/earshot`（第一次跑會自動下載模型）。
- 渲染混音後，將 MG 動作時間點（beats 嘅 t0＋cues）交俾佢：
  `earshot --threads 2 timeline 成品.mp4 --cues "12.0,13.1,..."`
- 睇三樣：
  1. **整體響度**：目標 -16 LUFS、true peak ≤ -1 dBTP。
  2. **對位**：`cue ... near / CHECK` 嘅位逐個睇，CHECK = 畫面有動作但冇聲起點。
  3. **疊聲**：同一刻多個 onset、或者音效蓋過人聲。
- 揀新音效入庫時可以用 `earshot match 檔案 "想要嘅效果描述"` 評分篩走唔夾嘅，最後由用戶耳仔決定。

## 原則
- 佢係提示唔係結論：聲音種類（CLAP 標籤）常錯，量度（時間、響度）先可信；改唔改由我哋判斷。
- 唔用 Earshot 自帶嘅音效：試過（彩虹飲食法），對比我哋庫 7 種全輸，太硬太機械，唔啱醫生科普片。
- 唔用 Openverse（伺服器唔穩、候選質素同庫差唔多）同 MMAudio（冇真實動作要配聲、要 GPU）。
