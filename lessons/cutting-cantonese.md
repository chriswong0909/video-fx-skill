# 剪停頓同口頭禪（廣東話）

工具：`tools/cut.py`（取代教學包嘅 cut-silences／cut-mistakes：嗰兩個只識英文，中文字會被當成空白）。

## 步驟
```bash
ffmpeg -i source.mp4 -ac 1 -ar 16000 work/audio.wav
python3 tools/asr.py <model_dir> work/audio.wav work/asr.json          # 見 lessons/asr-cantonese.md
python3 tools/cut.py analyze source.mp4 work/asr.json work --pace medium  # fast / medium / slow / off
# 睇 work/review.md → 決定 review 項目
python3 tools/cut.py set work/cuts.json 5,8 cut      # 或者 keep
python3 tools/cut.py apply source.mp4 work/cuts.json work/clean.mp4
```
之後調色、分鏡、字幕、HyperFrames **全部用 clean.mp4 + work/clean-transcript.json**，唔好再返去用原片時間。
要將原片時間轉做 clean 時間：`python3 tools/cut.py map work/edl.json 12.5`。

## 規則（已寫入工具）
| 類型 | 處理 |
|---|---|
| 頭尾空白 | 留 0.22s（頭）／0.34s（尾），其餘剪 |
| 停頓 | 超過門檻（fast 0.4／medium 0.55／slow 0.8）先剪；留呼吸 0.24s（≥2s 停頓）／0.20s（句尾）／0.14s（其他），fast ×0.8 |
| 停頓驗證 | 只喺 ffmpeg silencedetect（-35dB, ≥0.25s）確認係靜嘅範圍入面剪；ASR 話停但有聲 → 唔剪 |
| 呃／嗯／誒／唉 | 自動剪 |
| 即係／咁／然後／其實／就係／啦／呢／嘛 | 只列出（review），因為好多時係句子一部分 |
| 重複 2–4 字（口吃） | 自動剪第一次；相隔 > 1.2s 唔當口吃 |
| 重複單字 | review（可能係正常疊字） |
| 疊字白名單 | 慢慢、啱啱、好好、個個、少少、日日、成日… 唔當口吃 |
| 醫療限定詞 | 唔／冇／可能／或者／建議／除非／通常／副作用… 喺範圍入面 → 永遠降做 review |
| ASR 低信心（p < 0.10） | 只喺 review.md 底部列出，方便核對字幕，唔會剪 |

## 渲染
- 只 render 一次；每段接位 25ms 聲音淡入淡出，冇卜卜聲。
- 用整數影格切（trim start_frame/end_frame），影音唔會越剪越唔夾。
- 接位清單喺 `edl.json` 嘅 `joins`：分鏡時每個接位都要轉機位（W/M/C）或者用 FX-040 推入遮住。

## 幾時唔好剪
- 講者情緒位、刻意停頓（例如問完問題停一停）→ 喺 cuts.json 改做 keep。
- 節奏答「慢（保留講者）」→ `--pace slow` 或 `--pace off`（只剪頭尾同呃嗯）。
