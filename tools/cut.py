#!/usr/bin/env python3
"""cut.py — 廣東話口播剪停頓 + 口頭禪 + 口吃（重複字）工具

流程（每條片只 render 一次）：
  1. python3 tools/cut.py analyze source.mp4 asr.json work/ [--pace fast|medium|slow|off]
       → work/cuts.json（每個候選有 status: cut / review / keep）
       → work/review.md（人睇嘅表，逐項話點解剪）
  2. 睇 review.md，將 cuts.json 入面要剪嘅 review 改做 "cut"，唔剪嘅改 "keep"
     （或者：python3 tools/cut.py set work/cuts.json 5,7,9 cut）
  3. python3 tools/cut.py apply source.mp4 work/cuts.json clean.mp4
       → clean.mp4（每個接位 25ms 淡入淡出，冇卜卜聲）
       → work/clean-transcript.json（字嘅時間已經對返 clean.mp4）
       → work/edl.json（原片 ↔ clean 時間對照 + 接位 joins）
  之後所有步驟（調色、分鏡、字幕、HyperFrames）都用 clean.mp4 同 clean-transcript.json。

  （apply 預設做輕度人聲清理：高通 80Hz + 輕降噪 + loudnorm -16 LUFS；唔要就加 --no-voice）
  python3 tools/cut.py map work/edl.json 12.5   # 原片 12.5s 喺 clean 係幾多秒

原則：
  - 停頓只會喺 ffmpeg silencedetect（-35dB）確認真係靜嘅範圍入面剪，ASR 時間唔準都唔會剪到字。
  - 保留自然呼吸：停頓 ≥2s 留 0.24s，句尾留 0.20s，其他留 0.14s（fast 節奏 ×0.8）。
  - 自動剪：呃／嗯／誒 呢類純口頭聲；口吃重複（第二次緊接出現）。
  - 只列出唔自動剪：即係／咁／然後／其實／就係／啦 等（可能係句子一部分）。
  - 醫療限定詞（唔／冇／可能／建議／除非…）永遠唔自動剪；候選範圍包住佢就降做 review。
  - 所有剪位對齊影格。
兼容 ffmpeg 4.4。
"""
import json, os, re, subprocess, sys

# ---------------- 設定 ----------------
PACE_GAP = {"fast": 0.40, "medium": 0.55, "slow": 0.80, "off": None}
HEAD_PAD, TAIL_PAD = 0.22, 0.34
SILENCE_DB, SILENCE_MIN = -35, 0.25
FADE = 0.025

FILLER_CUT = {"呃", "嗯", "誒", "唉", "啊呃", "呃呃", "嗯嗯", "er", "erm", "um", "uh", "hmm"}
FILLER_REVIEW = {"即係", "咁", "咁樣", "然後", "其實", "就係", "啦", "呢", "嘛", "囉", "喎", "你知啦", "基本上", "so", "like"}
# 疊字：正常廣東話，唔當口吃
REDUP_OK = {"慢慢", "啱啱", "好好", "個個", "少少", "多多", "日日", "成日", "係係", "哈哈", "耐耐", "細細", "靜靜", "輕輕",
            "天天", "年年", "次次", "人人", "處處", "樣樣", "常常", "剛剛", "漸漸", "媽媽", "爸爸", "哥哥", "姐姐",
            "弟弟", "妹妹", "BB", "寶寶", "謝謝", "拜拜", "咪咪", "乜乜", "點點", "一一", "兩兩", "三三"}
# 醫療限定詞：出現喺候選範圍 → 永遠唔自動剪
PROTECT = ["唔", "冇", "無", "不", "未", "非", "可能", "或者", "大約", "大概", "一般", "通常", "建議", "除非", "未必",
           "少數", "部分", "有機會", "風險", "副作用", "醫生", "睇醫生", "求醫", "急症", "如果", "必須", "千祈", "切勿",
           "only", "not", "may", "might"]
PUNCT = "，。？！、；：,.!?;:「」『』“”\"'…—-（）() "
SENT_END = re.compile(r"[。？！.!?]$")


def sh(cmd, check=True):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if check and r.returncode != 0:
        sys.exit(f"指令失敗：{' '.join(cmd[:6])}…\n{r.stderr[-2000:]}")
    return r


def probe(video):
    r = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
            "stream=r_frame_rate:format=duration", "-of", "json", video])
    j = json.loads(r.stdout)
    num, den = j["streams"][0]["r_frame_rate"].split("/")
    return float(j["format"]["duration"]), float(num) / float(den)


def silences(video, db=SILENCE_DB, dmin=SILENCE_MIN):
    r = sh(["ffmpeg", "-hide_banner", "-nostats", "-i", video, "-vn", "-af",
            f"silencedetect=noise={db}dB:d={dmin}", "-f", "null", "-"], check=False)
    out, cur = [], None
    for line in r.stderr.splitlines():
        m = re.search(r"silence_start: ([\d.]+)", line)
        if m:
            cur = float(m.group(1))
        m = re.search(r"silence_end: ([\d.]+)", line)
        if m and cur is not None:
            out.append((cur, float(m.group(1))))
            cur = None
    if cur is not None:
        out.append((cur, 1e9))
    return out


def clean_text(t):
    return "".join(ch for ch in (t or "") if ch not in PUNCT).strip()


def load_words(path):
    """接受 asr.py 輸出 [{start,end,text,words:[{w,s,e,p}]}] 或 {words:[{text,start,end}]}"""
    j = json.load(open(path))
    words = []
    if isinstance(j, dict) and "words" in j:
        for w in j["words"]:
            if w.get("type", "word") != "word":
                continue
            words.append({"text": w["text"], "start": float(w["start"]), "end": float(w["end"]), "p": w.get("p", 1)})
    else:
        for seg in j:
            ws = seg.get("words") or []
            for i, w in enumerate(ws):
                t = w["w"]
                # 句尾標點：segment 最後一個字當句尾
                if i == len(ws) - 1 and not SENT_END.search(t.strip()):
                    t = t.rstrip() + "。"
                words.append({"text": t.strip(), "start": float(w["s"]), "end": float(w["e"]), "p": w.get("p", 1)})
    words = [w for w in words if w["end"] >= w["start"]]
    words.sort(key=lambda w: w["start"])
    for i, w in enumerate(words):
        w["i"] = i
        w["core"] = clean_text(w["text"])
    return words


def snap(t, fps, mode="round"):
    import math
    f = {"round": round, "in_start": lambda v: math.ceil(v - 1e-6), "in_end": lambda v: math.floor(v + 1e-6)}[mode]
    return round(f(t * fps) / fps, 4)


def inside_silence(a, b, sil, tol=0.04):
    """回傳 [a,b] 同靜音範圍嘅交集（最長嗰段），冇就 None"""
    best = None
    for s, e in sil:
        lo, hi = max(a, s + tol), min(b, e - tol)
        if hi - lo > 0.08 and (best is None or hi - lo > best[1] - best[0]):
            best = (lo, hi)
    return best


def protected(text):
    return any(p in text for p in PROTECT)


def char_stream(words):
    """將每個字拆成單一字元，按比例分配時間（whisper 廣東話有時一個 token 係幾個字）"""
    cs = []
    for w in words:
        core = w["core"]
        if not core:
            continue
        # 英文／數字當一粒
        parts = re.findall(r"[A-Za-z0-9]+|.", core)
        n = len(parts)
        d = (w["end"] - w["start"]) / max(n, 1)
        for k, ch in enumerate(parts):
            cs.append({"ch": ch, "start": w["start"] + k * d, "end": w["start"] + (k + 1) * d, "wi": w["i"],
                       "sent_end": k == n - 1 and bool(SENT_END.search(w["text"]))})
    return cs


def ctx(words, a, b, span=6):
    before = "".join(w["core"] for w in words if (w["start"] + w["end"]) / 2 < a)[-span:]
    inner = "".join(w["core"] for w in words if a <= (w["start"] + w["end"]) / 2 <= b)
    after = "".join(w["core"] for w in words if (w["start"] + w["end"]) / 2 > b)[:span]
    return f"{before}［{inner}］{after}"


# ---------------- analyze ----------------
def analyze(video, asr, outdir, pace="medium", gap=None):
    os.makedirs(outdir, exist_ok=True)
    dur, fps = probe(video)
    words = load_words(asr)
    if not words:
        sys.exit("ASR 冇字")
    sil = silences(video)
    gap = gap if gap is not None else PACE_GAP[pace]
    keep_scale = 0.8 if pace == "fast" else 1.0
    cands = []

    def add(kind, a, b, status, why, text=""):
        a, b = snap(max(0, a), fps, "in_start"), snap(min(dur, b), fps, "in_end")
        if b >= dur - 1.0 / fps:
            b = dur
        if b - a < 1.5 / fps:
            return
        if status == "cut" and protected(text):
            status, why = "review", why + "（包含限定詞，唔自動剪）"
        cands.append({"kind": kind, "start": a, "end": b, "status": status, "why": why, "text": text})

    # 1) 頭尾
    if words[0]["start"] - HEAD_PAD > 0.1:
        add("head", 0, words[0]["start"] - HEAD_PAD, "cut", "第一個字之前嘅空白")
    if dur - (words[-1]["end"] + TAIL_PAD) > 0.1:
        add("tail", words[-1]["end"] + TAIL_PAD, dur, "cut", "最後一個字之後嘅空白")

    # 2) 停頓（要 silencedetect 確認）
    if gap:
        for p, n in zip(words, words[1:]):
            g = n["start"] - p["end"]
            if g < gap:
                continue
            keep = (0.24 if g >= 2 else 0.20 if SENT_END.search(p["text"]) else 0.14) * keep_scale
            a, b = p["end"] + keep * 0.55, n["start"] - keep * 0.45
            hit = inside_silence(a, b, sil)
            if not hit:
                cands.append({"kind": "pause-unverified", "start": snap(a, fps), "end": snap(b, fps), "status": "keep",
                              "why": f"ASR 話停咗 {g:.2f}s 但 silencedetect 聽到有聲，唔剪", "text": ""})
                continue
            add("pause", hit[0], hit[1], "cut", f"停頓 {g:.2f}s → 留 {keep:.2f}s")

    # 3) 口頭禪
    for k, w in enumerate(words):
        c = w["core"].lower()
        if not c:
            continue
        prev_end = words[k - 1]["end"] if k else 0
        next_start = words[k + 1]["start"] if k + 1 < len(words) else dur
        a = max(prev_end, w["start"] - 0.03)
        b = min(next_start, w["end"] + 0.03)
        if c in FILLER_CUT:
            add("filler", a, b, "cut", f"口頭聲「{w['core']}」", w["core"])
        elif c in FILLER_REVIEW:
            add("filler?", a, b, "review", f"可能係口頭禪「{w['core']}」，睇上下文先決定", w["core"])

    # 4) 口吃／重複（1–4 字，第二次緊接出現就剪第一次）
    cs = char_stream(words)
    used = set()
    for n in (4, 3, 2, 1):
        for i in range(len(cs) - 2 * n + 1):
            if any(j in used for j in range(i, i + 2 * n)):
                continue
            A = "".join(c["ch"] for c in cs[i:i + n])
            B = "".join(c["ch"] for c in cs[i + n:i + 2 * n])
            if A != B or any(c["sent_end"] for c in cs[i:i + n - 1 + 1][:-1]):
                continue
            if cs[i + n - 1]["sent_end"]:
                continue  # 跨句唔算
            if n <= 2 and (A + B in REDUP_OK or A in REDUP_OK or A * 2 in REDUP_OK):
                continue
            if n == 1 and not re.match(r"[一-鿿]", A):
                continue
            a, b = cs[i]["start"], cs[i + n]["start"]
            gap2 = cs[i + n]["start"] - cs[i + n - 1]["end"]
            if gap2 > 1.2:
                continue
            status = "cut" if n >= 2 else "review"
            add("stutter", a, b, status, f"重複「{A}」×2，剪第一次" + ("（單字疊字，要聽下）" if n == 1 else ""), A)
            used.update(range(i, i + n))

    # 5) 低信心字（可能講錯／ASR 錯）→ 只提示
    for w in words:
        if w.get("p", 1) < 0.35 and len(w["core"]) >= 1:
            cands.append({"kind": "low-conf", "start": snap(w["start"], fps), "end": snap(w["end"], fps),
                          "status": "keep", "why": f"ASR 信心低 ({w['p']:.2f})，可能講錯或者聽錯，只供參考", "text": w["core"]})

    cands.sort(key=lambda c: (c["start"], c["end"]))
    for i, c in enumerate(cands, 1):
        c["id"] = i
        c["context"] = ctx(words, c["start"], c["end"])
    doc = {"source": os.path.abspath(video), "asr": os.path.abspath(asr), "duration": dur, "fps": fps,
           "pace": pace, "gap": gap, "silences": [[round(a, 3), round(min(b, dur), 3)] for a, b in sil],
           "words": [{k: w[k] for k in ("text", "start", "end")} for w in words], "cuts": cands}
    json.dump(doc, open(os.path.join(outdir, "cuts.json"), "w"), ensure_ascii=False, indent=1)
    write_review(doc, os.path.join(outdir, "review.md"))
    s = summary(doc)
    print(json.dumps(s, ensure_ascii=False))
    return doc


def merged_cuts(doc):
    rs = sorted([(c["start"], c["end"]) for c in doc["cuts"] if c["status"] == "cut"])
    out = []
    for a, b in rs:
        if out and a <= out[-1][1] + 0.02:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return out


def keeps_from(doc):
    dur, cur, ks = doc["duration"], 0.0, []
    for a, b in merged_cuts(doc):
        if a - cur >= 0.04:
            ks.append([cur, a])
        cur = max(cur, b)
    if dur - cur >= 0.04:
        ks.append([cur, dur])
    return ks


def summary(doc):
    by = {}
    for c in doc["cuts"]:
        k = f"{c['kind']}:{c['status']}"
        by[k] = by.get(k, 0) + 1
    ks = keeps_from(doc)
    new = sum(b - a for a, b in ks)
    return {"原長": round(doc["duration"], 2), "剪後": round(new, 2), "剪走": round(doc["duration"] - new, 2),
            "接位": max(len(ks) - 1, 0), "候選": by,
            "待決定": [c["id"] for c in doc["cuts"] if c["status"] == "review"]}


def write_review(doc, path):
    s = summary(doc)
    L = [f"# 剪輯候選（{os.path.basename(doc['source'])}）", "",
         f"原長 {s['原長']}s → 剪後 {s['剪後']}s（剪走 {s['剪走']}s，{s['接位']} 個接位）｜節奏 {doc['pace']}，停頓門檻 {doc['gap']}s", "",
         "狀態：**cut** 會剪｜**review** 要你決定｜keep 唔剪（只供參考）。改 cuts.json 或者用 `cut.py set`。", "",
         "| # | 類型 | 原片時間 | 長度 | 內容（［］= 會剪嘅位） | 原因 | 狀態 |", "|---|---|---|---|---|---|---|"]
    zh = {"head": "片頭空白", "tail": "片尾空白", "pause": "停頓", "pause-unverified": "停頓(未確認)", "filler": "口頭聲",
          "filler?": "口頭禪?", "stutter": "重複", "low-conf": "低信心"}
    for c in doc["cuts"]:
        st = {"cut": "**cut**", "review": "**review**", "keep": "keep"}[c["status"]]
        L.append(f"| {c['id']} | {zh.get(c['kind'], c['kind'])} | {c['start']:.2f}–{c['end']:.2f} | {c['end']-c['start']:.2f}s | "
                 f"{c['context']} | {c['why']} | {st} |")
    L += ["", "## 接位處理（剪完之後）",
          "每個接位喺 clean.mp4 會跳一下（jump cut）。分鏡時喺接位轉機位（W→M→C）或者用 FX-040 推入遮住；"
          "唔好兩個接位之間少過 1.2s 都用同一個機位。接位時間見 edl.json 嘅 `joins`。"]
    open(path, "w").write("\n".join(L) + "\n")


# ---------------- apply ----------------
VOICE = "highpass=f=80,afftdn=nr=8:nf=-45,loudnorm=I=-16:TP=-1.5:LRA=11"  # 輕度人聲清理


def apply(video, cutsfile, out, crf=18, preset="veryfast", voice=True):
    doc = json.load(open(cutsfile))
    fps = doc["fps"]
    ks = [[round(a * fps) / fps, round(b * fps) / fps] for a, b in keeps_from(doc)]
    ks = [k for k in ks if k[1] - k[0] >= 1 / fps]
    if not ks:
        sys.exit("冇嘢保留")
    outdir = os.path.dirname(os.path.abspath(cutsfile))
    parts, vl, al = [], "", ""
    for i, (a, b) in enumerate(ks):
        d = b - a
        fo = max(d - FADE, 0)
        fa, fb = round(a * fps), round(b * fps)  # 用整數影格，影音唔會越剪越唔夾
        a, b = fa / fps, fb / fps
        d = b - a
        fo = max(d - FADE, 0)
        parts.append(f"[0:v]trim=start_frame={fa}:end_frame={fb},setpts=PTS-STARTPTS[v{i}]")
        parts.append(f"[0:a]atrim=start={a:.6f}:end={b:.6f},asetpts=PTS-STARTPTS,"
                     f"afade=t=in:st=0:d={FADE},afade=t=out:st={fo:.4f}:d={FADE}[a{i}]")
        vl += f"[v{i}][a{i}]"
    fc = ";".join(parts) + f";{vl}concat=n={len(ks)}:v=1:a=1[v][ac]"
    total = sum(b - a for a, b in ks)
    fc += (f";[ac]{VOICE},aresample=48000,atrim=0:{total:.6f}[a]" if voice else ";[ac]anull[a]")
    fcf = os.path.join(outdir, "cut-filter.txt")
    open(fcf, "w").write(fc)
    sh(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", video, "-filter_complex_script", fcf,
        "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", preset, "-crf", str(crf), "-pix_fmt", "yuv420p",
        "-r", f"{doc['fps']:.4f}", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out])

    # EDL + 對返時間嘅字
    edl, t = [], 0.0
    for a, b in ks:
        edl.append({"src_start": round(a, 4), "src_end": round(b, 4), "out_start": round(t, 4), "out_end": round(t + b - a, 4)})
        t += b - a
    joins = [round(e["out_start"], 3) for e in edl[1:]]
    json.dump({"source": doc["source"], "output": os.path.abspath(out), "duration": round(t, 3), "segments": edl,
               "joins": joins}, open(os.path.join(outdir, "edl.json"), "w"), ensure_ascii=False, indent=1)
    words = []
    for w in doc["words"]:
        m = next((e for e in edl if e["src_start"] - 0.01 <= w["start"] and w["end"] <= e["src_end"] + 0.01), None)
        if not m:
            continue  # 被剪走
        off = m["out_start"] - m["src_start"]
        words.append({"text": w["text"], "start": round(max(w["start"] + off, m["out_start"]), 3),
                      "end": round(min(w["end"] + off, m["out_end"]), 3)})
    json.dump({"words": words, "audio_duration_secs": round(t, 3)},
              open(os.path.join(outdir, "clean-transcript.json"), "w"), ensure_ascii=False, indent=1)
    nd, _ = probe(out)
    print(json.dumps({"clean": out, "預計長度": round(t, 3), "實際長度": round(nd, 3), "接位": len(joins),
                      "字數": len(words)}, ensure_ascii=False))


def set_status(cutsfile, ids, status):
    doc = json.load(open(cutsfile))
    want = {int(x) for x in ids.split(",") if x.strip()}
    for c in doc["cuts"]:
        if c["id"] in want:
            c["status"] = status
    json.dump(doc, open(cutsfile, "w"), ensure_ascii=False, indent=1)
    write_review(doc, os.path.join(os.path.dirname(os.path.abspath(cutsfile)), "review.md"))
    print(json.dumps(summary(doc), ensure_ascii=False))


def map_time(edlfile, t):
    edl = json.load(open(edlfile))
    for e in edl["segments"]:
        if e["src_start"] <= t <= e["src_end"]:
            print(round(e["out_start"] + t - e["src_start"], 3))
            return
    print("呢個時間已經被剪走")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)
    cmd = a[0]
    if cmd == "analyze":
        pace, gap = "medium", None
        rest = a[1:]
        if "--pace" in rest:
            i = rest.index("--pace"); pace = rest[i + 1]; del rest[i:i + 2]
        if "--gap" in rest:
            i = rest.index("--gap"); gap = float(rest[i + 1]); del rest[i:i + 2]
        analyze(rest[0], rest[1], rest[2], pace, gap)
    elif cmd == "apply":
        apply(a[1], a[2], a[3], voice="--no-voice" not in a)
    elif cmd == "set":
        set_status(a[1], a[2], a[3])
    elif cmd == "map":
        map_time(a[1], float(a[2]))
    else:
        sys.exit(__doc__)
