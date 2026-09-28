# usage: python3 tools/asr.py <model_dir> <audio.wav> <out.json> [language=yue] [prompt]
# model: https://huggingface.co/deepdml/faster-whisper-large-v3-turbo-ct2 (see lessons/asr-cantonese.md)
# audio: ffmpeg -i in.mp4 -ac 1 -ar 16000 audio.wav
import json, sys
from faster_whisper import WhisperModel
model_dir, wav, out = sys.argv[1:4]
lang = sys.argv[4] if len(sys.argv) > 4 else "yue"
prompt = sys.argv[5] if len(sys.argv) > 5 else "以下係香港人用廣東話講嘢。"
m = WhisperModel(model_dir, device="cpu", compute_type="int8", cpu_threads=4)
segs, info = m.transcribe(wav, language=lang, word_timestamps=True, beam_size=5, vad_filter=False, initial_prompt=prompt)
res = []
for s in segs:
    res.append({"start": s.start, "end": s.end, "text": s.text,
                "words": [{"w": w.word, "s": w.start, "e": w.end, "p": w.probability} for w in s.words]})
    print(f"{s.start:.2f}-{s.end:.2f} {s.text}", flush=True)
json.dump(res, open(out, "w"), ensure_ascii=False, indent=1)
