# Dr Cheryl 骨質疏鬆（2026-10-15 正式版）
Healthy Days × Kallaway 淺色，95.9 秒 9:16，語速 1.1x，BGM Clock Struck Twice 15%。

重建次序（雲端工作區會被重置，一定要喺用戶電腦留低呢套）：
1. 調色：`ffmpeg -i clean.mp4 -vf "$(cat vf.txt)" … assets/graded.mp4`
2. `sil.txt`（silencedetect -35dB d=0.15）→ 跑 plan（見 rebuild 前段，或直接用 plan.json）
3. `python3 segs.py` → map.json、assets/fast_full.mp4（剪位 + 0.1 秒溶接 + 1.1x）
4. 剪走長大衣段：fast_full 第 539–734 格（聲音按樣本切）→ assets/fast.mp4
5. `python3 rebuild.py` → beats.json、cam.json、caps.py、sfx-events.json
6. `python3 mg2.py`（5 個精緻 2D MG）→ `python3 build.py`（含 38 螢光筆 highlight()）
7. sfx_plan → sfx mix → BGM 0.15 → render → mux

字卡效果：03 Text Stamp（開場）、29 Odometer（25%）、38 Highlight Text（關鍵詞／全屏大字）。
字幕：#186baa 方角，白字，≤10 字。
