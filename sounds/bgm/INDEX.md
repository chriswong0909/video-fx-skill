# Healthy Days 背景音樂（BGM）

用戶提供嘅三條，**一條片揀一條由頭用到尾，音量 10%，頭 0.6 秒淡入、尾 2 秒淡出，唔好中途換歌**。
檔案位置：本資料夾（`sounds/bgm/`）。用 skill 時**直接用呢度嘅檔案，唔使問用戶 BGM 喺邊**。

| 檔案 | 曲名 | 作者（版權協會） | 原檔名 |
|---|---|---|---|
| `breakthrough-technology.mp3` | Breakthrough Technology | Kenneth E. Belcher (ASCAP)，Sonic Station SOS 001 005 | BREAKTHROUGH_TECHNOLOGY_(A)_…SOS_001_005.mp3 |
| `clock-struck-twice.mp3` | Clock Struck Twice | Matthew St. Laurent (ASCAP)，Stay Tuned Music STAY 010 007 | CLOCK_STRUCK_TWICE_(A)_…STAY_010_007.mp3 |
| `only-in-dreams.mp3` | Only In Dreams | Marco DiFelice (SOCAN)，Zero Degrees ZRO 029 058 | ONLY_IN_DREAMS_(B)_…ZRO_029_058.mp3 |

授權：三條都已取得使用版權（Healthy Days），可用於日常製作。
混音例子：`ffmpeg -i voice.wav -i bgm.mp3 -filter_complex "[1:a]volume=0.10,afade=t=in:d=0.6,afade=t=out:st=<總長-2>:d=2[b];[0:a][b]amix=inputs=2:duration=first:normalize=0[a]"`
