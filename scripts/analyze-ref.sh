#!/usr/bin/env bash
# usage: bash scripts/analyze-ref.sh ref.mp4 out_dir [fps=2]
set -euo pipefail
IN="$1"; OUT="$2"; FPS="${3:-2}"; mkdir -p "$OUT"
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")
ffprobe -v error -show_entries stream=codec_type,width,height,r_frame_rate:format=duration -of compact "$IN" > "$OUT/info.txt"
N=$(python3 -c "import math;print(math.ceil($DUR*$FPS))"); ROWS=$(( (N+7)/8 ))
ffmpeg -v error -y -i "$IN" -vf "fps=$FPS,scale=270:-2,drawtext=text='%{pts\:hms}':x=5:y=5:fontsize=20:fontcolor=yellow:box=1:boxcolor=black,tile=8x$ROWS" -frames:v 1 "$OUT/sheet.jpg"
ffmpeg -v error -y -i "$OUT/sheet.jpg" -vf "scale='min(1200,iw)':-2" "$OUT/sheet-small.jpg"
ffmpeg -v info -i "$IN" -vf "select='gt(scene,0.25)',showinfo" -f null - 2>&1 | grep -o 'pts_time:[0-9.]*' | cut -d: -f2 > "$OUT/cuts.txt" || true
ffmpeg -i "$IN" -af silencedetect=n=-35dB:d=0.25 -f null - 2>&1 | grep -o 'silence_[a-z]*: [0-9.]*' > "$OUT/silence.txt" || true
echo "duration=$DUR cuts=$(wc -l < "$OUT/cuts.txt") -> $OUT"
