# 人像分層補光（技術筆記；原 FX-011 已移除）

- RobustVideoMatting `rvm_mobilenetv3_fp32.onnx`（GitHub releases, 15MB），onnxruntime CPU，`downsample_ratio=0.25`。
- 約 0.28 秒／幀（1080×1920，4 核）。分段處理時每段前面多跑 30 幀暖機，接駁位冇閃。
- 邊位白邊：用 RVM 輸出嘅 `fgr`（去色溢前景）代替原圖做邊位像素。
- 補光要用 screen 式（`fg + key*k*(1-fg)`）避免臉部過曝；主光 0.08、輪廓光 0.10 已足夠。
- 限制：只係分層調色，唔可以改光向、陰影、眼神光；前景枱會被當背景虛化。
