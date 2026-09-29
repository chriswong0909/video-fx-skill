#!/usr/bin/env python3
"""presets.py — 風格預設工具
  python3 scripts/presets.py build      # preset.json → tokens.css + DESIGN.md；再更新 effects/*/effect.md 嘅 family 標籤
  python3 scripts/presets.py tokenize   # 將 effects/*/snippet.html 轉用標準 tokens（可重複行，唔會重複改）
  python3 scripts/presets.py report     # 每個效果：屬邊個預設、仲有幾多個寫死嘅顏色
"""
import glob, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def presets():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "presets", "SP-*", "preset.json"))):
        p = json.load(open(f))
        p["_dir"] = os.path.dirname(f)
        out.append(p)
    return out


def build():
    for p in presets():
        t, d = p["tokens"], p["_dir"]
        open(os.path.join(d, "tokens.css"), "w").write(
            f"""/* {p['id']} {p['name']} — 由 preset.json 生成（python3 scripts/presets.py build）；品牌檔可以喺之後覆蓋顏色 */
:root{{
  --c-bg:{t['bg']}; --c-surface:{t['surface']}; --c-text:{t['text']};
  --c-accent:{t['accent']}; --c-alert:{t['alert']}; --c-positive:{t['positive']};
  --c-caption-box:{t['caption_box']}; --c-caption-text:{t['caption_text']};
  --f-display:{t['f_display']}; --f-body:{t['f_body']}; --f-num:{t['f_num']};
  --fs-hero:150px; --fs-sub:72px; --fs-label:64px; --fs-caption:80px; --fs-foot:52px;
  --ease-out:{t['ease_out']}; --ease-pop:{t['ease_pop']}; --ease-move:{t['ease_move']}; --ease-in:{t['ease_in']};
  --dur-in:{t['dur_in']}; --dur-out:{t['dur_out']}; --dur-move:{t['dur_move']}; --stagger:{t['stagger']};
}}
""")
        cm = "\n".join(f"- `--c-{k}` {t[k]}：{v}" for k, v in p["colour_meaning"].items())
        sfx = p["sfx"]
        md = f"""# {p['id']} {p['name']}（{p['en']}）

適合：{'、'.join(p['for_types'])}｜情緒：{p['mood_zh']}

## 一套過決定
| 項目 | 設定 |
|---|---|
| 調色 | {p['grade']}（備選 {'、'.join(p['grade_alt'])}） |
| 字幕 | {'／'.join(p['captions'])}（全片只用一款） |
| 轉場 | {'、'.join(p['transitions'])}（最多兩款） |
| 聲效 | {sfx['pack']}：{'、'.join(sfx['categories'])}｜預設密度 {sfx['density']}｜冇背景音樂 |
| 字體 | 標題 {t['f_display']}／內文 {t['f_body']} |
| 緩動 | out {t['ease_out']}｜pop {t['ease_pop']}｜move {t['ease_move']}｜in {t['ease_in']} |

## 色彩意思
{cm}

## 效果白名單（{len(p['effects'])} 個）
{'、'.join(p['effects'])}

白名單以外嘅效果要喺分鏡寫理由，而且要用返本預設嘅 tokens。

## 唔好
""" + "\n".join("- " + x for x in p["dont"]) + "\n"
        open(os.path.join(d, "DESIGN.md"), "w").write(md)
    tag()


def tag():
    fam = {}
    for p in presets():
        for e in p["effects"]:
            fam.setdefault(e, []).append(p["id"])
    none = []
    for f in sorted(glob.glob(os.path.join(ROOT, "effects", "FX-*", "effect.md"))):
        s = open(f).read()
        m = re.match(r"^---\n(.*?)\n---", s, re.S)
        if not m:
            continue
        fm = m.group(1)
        eid = re.search(r"^id:\s*(\S+)", fm, re.M).group(1)
        line = f"family: [{', '.join(fam.get(eid, []))}]"
        if re.search(r"^family:.*$", fm, re.M):
            fm2 = re.sub(r"^family:.*$", line, fm, flags=re.M)
        else:
            fm2 = re.sub(r"^(category:.*)$", r"\1\n" + line, fm, count=1, flags=re.M)
        if fm2 != fm:
            open(f, "w").write(s.replace(fm, fm2, 1))
        if not fam.get(eid):
            none.append(eid)
    print(f"family 標籤已更新；未屬任何預設：{len(none)} 個 {' '.join(none)}")


PREAMBLE = ("<script>/* tokens 讀取器（presets/README.md）*/window.EASE=window.EASE||(()=>{const g=(n,d)=>(getComputedStyle(document.documentElement)"
            ".getPropertyValue('--ease-'+n).trim()||d);return{out:g('out','power3.out'),pop:g('pop','back.out(1.8)'),move:g('move','power2.inOut'),in:g('in','power2.in')}})();"
            "window.DUR=window.DUR||(()=>{const g=(n,d)=>{const v=parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--'+n));return isNaN(v)?d:v};"
            "return{in:g('dur-in',.35),out:g('dur-out',.25),move:g('dur-move',.6),stagger:g('stagger',.08)}})();</script>")

EASE_MAP = [
    (r"ease:'(?:power[1-4]|expo|circ|quad|cubic)\.out'", "ease:EASE.out"),
    (r"ease:'back\.out(?:\([\d.]+\))?'", "ease:EASE.pop"),
    (r"ease:'(?:power[1-4]|sine|expo|circ)\.inOut'", "ease:EASE.move"),
    (r"ease:'(?:power[1-4]|expo|circ)\.in'", "ease:EASE.in"),
]


def tokenize():
    changed = 0
    for f in sorted(glob.glob(os.path.join(ROOT, "effects", "FX-*", "snippet.html"))):
        s0 = s = open(f).read()
        s = s.replace("var(--brand,", "var(--c-accent,").replace("var(--brand)", "var(--c-accent)")
        s = s.replace("var(--accent,", "var(--c-alert,").replace("var(--accent)", "var(--c-alert)")
        s = s.replace("var(--caption-box,", "var(--c-caption-box,")
        # 字體：'SansTC' → var(--f-body,'SansTC')；'SerifTC' → var(--f-display,'SerifTC')（已經包咗就唔再包）
        s = re.sub(r"(?<!,)(['\"])SansTC\1", lambda m: f"var(--f-body,{m.group(0)})", s)
        s = re.sub(r"(?<!,)(['\"])SerifTC\1", lambda m: f"var(--f-display,{m.group(0)})", s)
        # JS 入面嘅 fontFamily:'SansTC' 唔可以用 var() → 還原
        s = re.sub(r"fontFamily:var\(--f-(?:body|display),(['\"]\w+['\"])\)", r"fontFamily:\1", s)
        n_ease = 0
        for pat, rep in EASE_MAP:
            s, k = re.subn(pat, rep, s)
            n_ease += k
        if "EASE." in s and "window.EASE=" not in s:
            s = PREAMBLE + "\n" + s
        if s != s0:
            open(f, "w").write(s)
            changed += 1
    print(f"tokenize：改咗 {changed} 個 snippet")


def report():
    fam = {}
    for p in presets():
        for e in p["effects"]:
            fam.setdefault(e, []).append(p["id"])
    rows = []
    for f in sorted(glob.glob(os.path.join(ROOT, "effects", "FX-*", "snippet.html"))):
        eid = re.search(r"(FX-\d{3})", f).group(1)
        s = open(f).read()
        css_hex = len(re.findall(r"(?<!,)#[0-9a-fA-F]{6}\b", re.sub(r"var\([^)]*\)", "", s)))
        toks = len(re.findall(r"var\(--(?:c|f|fs|ease|dur)-", s)) + s.count("EASE.")
        rows.append((eid, ",".join(fam.get(eid, [])) or "—", toks, css_hex))
    print("| 效果 | 預設 | token 用量 | 寫死顏色 |\n|---|---|---|---|")
    for r in rows:
        print(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} |")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    {"build": build, "tag": tag, "tokenize": tokenize, "report": report}.get(cmd, lambda: print(__doc__))()
