#!/usr/bin/env python3
"""外部效果來源（text-motion-40）查詢 + 出配對表。見 workflow/external-effects.md

  python3 tools/ext_effects.py list [--use 強調] [--cat IMPACT|FLOW|DEPTH|SWITCH|STYLE]   # 列款（⚠＝冇睇圖唔准用）
  python3 tools/ext_effects.py show 29                  # 提示詞、分格圖／短片路徑、注意
  python3 tools/ext_effects.py table matches.json out.html   # 出配對表（分格圖內嵌 base64），再用 Artifact 發佈
  python3 tools/ext_effects.py fontcheck 29 "65歲以上女性"      # 逐個原作字體檢查缺字（日文字體可能缺繁體字）
  python3 tools/ext_effects.py brandfont --project DIR --text "歲"   # 缺字 fallback：補 Noto Sans TC 900 子集到 DIR/assets/fonts/sans900.woff2（保留舊字）
做卡（原作程式碼做起點）：python3 tools/cards.py adapt --ext 29 [--style kallaway]；之後 cards.py use 會自動複製字體、檢查缺字同顏色對比。

來源路徑：環境變數 TM40（預設 ~/Documents/GitHub/text-motion-40）。本機冇就用 GitHub MCP 讀 chriswong0909/text-motion-40。

matches.json：
{"project": "骨質疏鬆", "brand": "Healthy Days（Kallaway 淺色）",
 "items": [{"slot": "hook", "line": "原句", "t": "0:08",
            "cands": [{"id": "29", "why": "點解 match", "scene": "呢位要畫咩場景（背景／主體圖形／字點排）"}, {"id": "03", "why": "…"}]}],
 "viewed": ["03", "29"],            # 睇過分格圖嘅款（用嚟寫 Treatment）
 "none_reason": ""}                 # 全部唔用就寫原因
"""
import sys, os, json, base64, subprocess, tempfile, html

TM = os.path.expanduser(os.environ.get("TM40", "~/Documents/GitHub/text-motion-40"))
if not os.path.exists(os.path.join(TM, "effects.json")):   # Cowork 本機 VM：資料夾掛喺 ~/mnt/Documents
    _alt = os.path.expanduser("~/mnt/Documents/GitHub/text-motion-40")
    if os.path.exists(os.path.join(_alt, "effects.json")): TM = _alt
WARN = {"01", "02", "17", "18", "20", "33"}

def load():
    p = os.path.join(TM, "effects.json")
    if not os.path.exists(p):
        sys.exit(f"搵唔到 {p}；用 GitHub MCP 讀 chriswong0909/text-motion-40，或設 TM40=路徑")
    return {e["id"]: e for e in json.load(open(p, encoding="utf-8"))}

def eff(E, i):
    i = str(i).zfill(2)
    if i not in E: sys.exit(f"冇編號 {i}")
    return E[i]

def cmd_list(args):
    E = load(); use = cat = None
    if "--use" in args: use = args[args.index("--use") + 1]
    if "--cat" in args: cat = args[args.index("--cat") + 1].upper()
    for e in E.values():
        if use and use not in e["use"] + e["name_zh"] + e["prompt"]: continue
        if cat and e["category"] != cat: continue
        w = "⚠" if e["id"] in WARN else " "
        print(f'{e["id"]} {w} {e["name_en"]}（{e["name_zh"]}）｜{e["category_zh"]}｜用於 {e["use"]}')

def cmd_show(args):
    e = eff(load(), args[0])
    print(json.dumps(e, ensure_ascii=False, indent=1))
    print("分格圖:", os.path.join(TM, e["strip"])); print("短片:", os.path.join(TM, e["clip"]))
    if e.get("code"): print("程式碼:", os.path.join(TM, e["code"]), "＋", os.path.join(TM, "code", "_header.js"), "｜字體:", "、".join(e.get("fonts", [])), "｜原作色:", e.get("default_colors"))
    if e["id"] in WARN: print("⚠ 冇睇分格圖唔准用")

def thumb(path, w=1000):
    with tempfile.TemporaryDirectory() as d:
        o = os.path.join(d, "t.jpg")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-vf", f"scale={w}:-2", "-q:v", "4", o], check=True)
        return base64.b64encode(open(o, "rb").read()).decode()

CSS = """<style>
:root{--bg:#fff;--fg:#1b2733;--mute:#5d6b78;--line:#dfe5ea;--card:#f5f8fa;--acc:#186baa;--warn:#b45309}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#10161c;--fg:#e8eef3;--mute:#9aa8b4;--line:#2a3541;--card:#18212a;--acc:#6db3ea;--warn:#f0a35b}}
:root[data-theme="dark"]{--bg:#10161c;--fg:#e8eef3;--mute:#9aa8b4;--line:#2a3541;--card:#18212a;--acc:#6db3ea;--warn:#f0a35b}
body{background:var(--bg);color:var(--fg);font:16px/1.6 system-ui,-apple-system,"PingFang HK","Noto Sans TC",sans-serif;margin:0}
main{max-width:920px;margin:0 auto;padding:24px 16px 64px}
h1{font-size:24px;margin:0 0 4px}.sub{color:var(--mute);margin:0 0 24px}
.slot{border:1px solid var(--line);border-radius:12px;background:var(--card);padding:16px;margin:0 0 20px}
.slot h2{font-size:18px;margin:0 0 4px}.line{color:var(--mute);margin:0 0 12px}
.cand{border-top:1px solid var(--line);padding-top:12px;margin-top:12px}
.cand h3{font-size:16px;margin:0 0 4px}.cand h3 span{color:var(--acc)}
.cand p{margin:0 0 8px}.cand img{width:100%;border-radius:8px;display:block}
.warn{color:var(--warn);font-weight:600}.note{border-left:4px solid var(--acc);padding:4px 12px;margin:0 0 20px}
</style>"""

def cmd_table(args):
    E = load(); m = json.load(open(args[0], encoding="utf-8")); out = args[1]
    h = [CSS, "<main>", f"<h1>外部效果配對表｜{html.escape(m.get('project',''))}</h1>",
         f"<p class='sub'>風格包基礎：{html.escape(m.get('brand',''))} ｜來源：text-motion-40 ｜每位最多 2 個候選，請批或改</p>"]
    for it in m["items"]:
        h.append(f"<section class='slot'><h2>{html.escape(it['slot'])}　<span style='color:var(--mute);font-weight:400'>{html.escape(it.get('t',''))}</span></h2>"
                 f"<p class='line'>原句：{html.escape(it['line'])}</p>")
        if not it["cands"]:
            h.append("<p>冇適合候選：用風格包本身嘅卡。" + html.escape(it.get("why", "")) + "</p>")
        for c in it["cands"][:2]:
            e = eff(E, c["id"]); b64 = thumb(os.path.join(TM, e["strip"]))
            w = " <span class='warn'>⚠ 已睇分格圖</span>" if e["id"] in WARN else ""
            h.append(f"<div class='cand'><h3><span>#{e['id']}</span> {html.escape(e['name_en'])}（{html.escape(e['name_zh'])}）{w}</h3>"
                     f"<p><b>點解 match：</b>{html.escape(c['why'])}</p>"
                     + (f"<p><b>場景設計：</b>{html.escape(c['scene'])}</p>" if c.get("scene") else "") +
                     f"<img alt='{html.escape(e['name_en'])} 分格圖' src='data:image/jpeg;base64,{b64}'></div>")
        h.append("</section>")
    if m.get("none_reason"):
        h.append(f"<p class='note'><b>一款都唔用：</b>{html.escape(m['none_reason'])}</p>")
    h.append("</main>")
    open(out, "w", encoding="utf-8").write("\n".join(h)); print("✓", out, os.path.getsize(out) // 1024, "KB")

# ---------- 做卡：用原作程式碼做起點（2026-10-16，text-motion-40 加咗 code/、fonts/、PROMPT_TEMPLATE.md） ----------
import re, shutil, datetime

FKEY = {"dela": "Dela_Gothic_One.ttf", "antique": "Zen_Antique.ttf", "reggae": "Reggae_One.ttf", "rock": "RocknRoll_One.ttf",
        "dot": "DotGothic16.ttf", "train": "Train_One.ttf", "rampart": "Rampart_One.ttf", "zen": "Zen_Kaku_Gothic_New.ttf"}
FAM = {"dela": "Dela Gothic One", "antique": "Zen Antique", "reggae": "Reggae One", "rock": "RocknRoll One",
       "dot": "DotGothic16", "train": "Train One", "rampart": "Rampart One", "zen": "Zen Kaku Gothic New"}
HEADER_TL = "const TL = () => gsap.timeline({ repeat: 5 });"
HEADER_TL_NEW = "const TL = () => gsap.timeline({ paused: true }); /* 原作係 repeat:5（預覽用）；播放次數改由 data-freeze／data-loops 控制 */"
MIN_FX_PX = 76

def code_file(eid):
    eid = str(eid).zfill(2); d = os.path.join(TM, "code")
    if not os.path.isdir(d): sys.exit(f"text-motion-40 冇 code/（{d}）：先 git pull，或用 GitHub MCP 讀 chriswong0909/text-motion-40")
    fs = [f for f in sorted(os.listdir(d)) if f.startswith(eid + "_") and f.endswith(".js")]
    if not fs: sys.exit(f"冇 #{eid} 嘅程式碼")
    return os.path.join(d, fs[0])

def scan(src, scale):
    sizes = sorted({float(x) for x in re.findall(r"font:\s*[\w.-]+\s+(\d+(?:\.\d+)?)px", src)} |
                   {float(x) for x in re.findall(r"font-size:\s*(\d+(?:\.\d+)?)px", src)})
    demo = []
    for m in re.finditer(r"'([^'\n$]{1,24})'|\"([^\"\n$]{1,24})\"", src):
        s = m.group(1) or m.group(2)
        if (re.search(r"[　-鿿＀-￯]", s) or re.fullmatch(r"\d{2,}", s)) and s not in demo: demo.append(s)
    return {"fonts": sorted(set(re.findall(r"F\.(\w+)", src)) & set(FKEY)),
            "sizes": [(s, round(s * scale, 1)) for s in sizes],
            "small": [(s, round(s * scale, 1)) for s in sizes if s * scale < MIN_FX_PX],
            "random": "Math.random" in src,
            "repeat": re.findall(r"repeat:\s*-?\d+", src),
            "timers": [t for t in ("setTimeout", "setInterval", "requestAnimationFrame", "Date.now", "performance.now") if t in src],
            "demo": demo[:12]}

def cov(key):
    try: from fontTools.ttLib import TTFont
    except ImportError: sys.exit("缺 fonttools：pip install fonttools")
    return set(TTFont(os.path.join(TM, "fonts", FKEY[key])).getBestCmap())

def missing(text, keys):
    out = {}
    for k in keys:
        c = cov(k); m = sorted({ch for ch in text if not ch.isspace() and ord(ch) not in c})
        if m: out[k] = "".join(m)
    return out

def cmd_fontcheck(args):
    """fontcheck 編號 "要顯示嘅字" → 逐個原作字體檢查缺字"""
    eid, text = str(args[0]).zfill(2), "".join(args[1:])
    keys = scan(open(code_file(eid), encoding="utf-8").read(), 1)["fonts"]
    print(f"#{eid} 用到字體：{', '.join(FAM[k] for k in keys) or '（冇用 F.*）'}")
    miss = missing(text, keys)
    for k in keys: print(f"  {FAM[k]:<22}", "缺字：" + miss[k] if k in miss else "✓ 齊")
    if miss: print("→ 缺字嗰段文字改用品牌中文字體（同粗度，Noto Sans TC 900），唔好一句混兩款；用 `ext_effects.py brandfont --project DIR --text …` 補字體子集")
    else: print("→ 原作字體齊，唔使 fallback")

def brand_chars(path):
    """專案 sans900.woff2 已有嘅字；讀唔到（冇檔／冇 brotli）回傳 None"""
    if not os.path.exists(path): return set()
    try:
        from fontTools.ttLib import TTFont
        return {chr(c) for c in TTFont(path).getBestCmap()}
    except Exception: return None

def cmd_brandfont(args):
    """brandfont --project DIR --text "字…" → 下載／補 Noto Sans TC 900 子集到 DIR/assets/fonts/sans900.woff2（保留舊有字）"""
    import urllib.request, urllib.parse
    a = dict(zip(args[::2], args[1::2])); proj = os.path.expanduser(a.get("--project", ".")); text = a.get("--text", "")
    dst = os.path.join(proj, "assets", "fonts", "sans900.woff2"); old = ""
    if os.path.exists(dst):
        try:
            from fontTools.ttLib import TTFont
            old = "".join(chr(c) for c in TTFont(dst).getBestCmap() if c > 32)
        except Exception as e:
            sys.exit(f"讀唔到現有 {dst} 嘅字（{e}）；pip install brotli fonttools 再試，免得蓋走舊字")
    allt = "".join(sorted(set(old + text + "0123456789%.,-+ ")))
    url = "https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@900&text=" + urllib.parse.quote(allt)
    ua = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    css = urllib.request.urlopen(urllib.request.Request(url, headers=ua), timeout=30).read().decode()
    m = re.search(r"url\((https://[^)]+)\) format\('(\w+)'\)", css)
    if not m or m.group(2) != "woff2": sys.exit("Google Fonts 冇俾 woff2：" + css[:200])
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, "wb").write(urllib.request.urlopen(urllib.request.Request(m.group(1), headers=ua), timeout=60).read())
    print(f"✓ {dst}（{len(allt)} 個字，其中新增 {len(set(text) - set(old))} 個）")

# --- 顏色：由品牌 tokens 讀 --ext-bg/fg/hi/ink 角色，檢查對比 ---
ROLE_VARS = {"bg": "--ink", "fg": "--paper", "hi": "--accent-2", "ink": "--ink"}

def css_vars(css):
    v = {}
    for k, val in re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", css): v[k] = val.strip()
    return v

def resolve(v, name, depth=0):
    val = v.get(name, "")
    m = re.match(r"var\((--[\w-]+)(?:\s*,\s*([^)]+))?\)", val)
    if m and depth < 6: return resolve(v, m.group(1), depth + 1) or (m.group(2) or "").strip()
    return val

def lum(hexc):
    h = hexc.lstrip("#"); h = "".join(ch * 2 for ch in h) if len(h) == 3 else h
    r, g, b = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    f = lambda x: x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)

def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + 0.05) / (lb + 0.05)

def check_colors(css, overrides=None):
    """css＝style tokens＋品牌 tokens 串埋；overrides＝{'bg':'#..'}。回傳 (colors, 報告行)"""
    v = css_vars(css); c = {}
    for role, var in ROLE_VARS.items():
        c[role] = (overrides or {}).get(role) or resolve(v, var)
    lines, ok = [], True
    for role in c:
        if not re.match(r"^#[0-9a-fA-F]{3,6}$", c[role] or ""): lines.append(f"! 角色 {role} 解析唔到顏色（{c[role]!r}）：用 --colors {role}=#hex 指定"); ok = False
    if ok:
        for a, b, what in (("hi", "bg", "強調字／標籤 對 底"), ("fg", "bg", "主色塊 對 底"), ("ink", "fg", "色塊上嘅字 對 色塊")):
            r = ratio(c[a], c[b]); lines.append(f"  對比 {what}：{c[a]} / {c[b]} = {r:.1f}:1 " + ("✓" if r >= 4.5 else "✗ <4.5，手機細畫面睇唔清；用 --colors 換色"))
    return c, lines

# --- 砌卡 ---
CARD = r'''<!doctype html>
<!--
  text-motion-40 #@@ID@@ @@EN@@（@@ZH@@）· 外部效果卡 · 由 `cards.py adapt --ext @@ID@@` 產生（@@DATE@@）
  原作程式碼：text-motion-40/code/@@CODE@@ ＋ code/_header.js，全部包喺 IIFE（function scope）入面，唔會同其他卡／主檔撞名。
  已做：TL() 由 repeat:5 改 paused；播放次數由 data-freeze／data-loops 控制；顏色讀 ext-bg／ext-fg／ext-hi／ext-ink（預設跟品牌 tokens）；
        舞台 487×160 成個放大 @@SC@@ 倍；缺字 fallback 用 FF(字體key, 文字)。
  仍要人手做：
   1. 換字：示範字 @@DEMO@@ → 抽成 data-slot，按字數調字級同位置，唔好出界。
   2. 字級：效果字要 ≥ 76px（舞台單位 ×@@SC@@）。@@SMALL@@
   3. data-freeze（凍結喺原作第幾秒；預設 @@FREEZE@@，0＝播完整個 2 秒循環）或 data-loops（1＝只播一次，數字，auto＝按 dur）。
   4. hyperframes snapshot 每 0.75 秒 8 格，同 text-motion-40/strips/@@STRIP@@ 並排對比；批咗 cards.py verify @@CARD@@ --source text-motion-40#@@ID@@
  @@WARN@@
-->
<html>
  <head>
    <meta charset="utf-8" />
    <link rel="stylesheet" href="../tokens.css" />
    <style>
@@FONTFACES@@
      html, body { margin: 0; background: transparent; }
      #@@NAME@@ { position: absolute; inset: 0; width: 1080px; height: 1920px; background: transparent; overflow: hidden;
        --ext-bg: var(--ink, #0B2A3A); --ext-fg: var(--paper, #FFFFFF); --ext-hi: var(--accent-2, #13B8D0); --ext-ink: var(--ink, #0B2A3A); }
      #@@NAME@@ .panel { position: absolute; left: 53px; top: @@TOP@@px; width: @@PANELW@@px; height: @@PANELH@@px; border-radius: 40px; overflow: hidden;
        box-shadow: var(--glass-shadow, 0 18px 48px rgba(11, 42, 58, 0.18)); }
      #@@NAME@@ .stage { position: absolute; left: 0; top: 0; width: 487px; height: 160px; transform: scale(@@SC@@); transform-origin: 0 0; overflow: hidden; }
      #@@NAME@@ .pos, #@@NAME@@ .sl { display: none; }
    </style>
  </head>
  <body>
    <div id="@@NAME@@" data-composition-id="@@NAME@@" data-start="0" data-width="1080" data-height="1920">
      <i class="pos" data-slot="top"></i>
      <div class="panel"><div class="stage"></div></div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <script>
      window.__timelines = window.__timelines || {};
      (function () {
        const ROOT = document.querySelector('[data-composition-id="@@NAME@@"]');
        const CUES = (ROOT.dataset.cues || '').split(',').filter(Boolean).map(Number);
        const DUR = +ROOT.dataset.dur || 4;
        const SPEED = +ROOT.dataset.speed || 1;
        const LOOPS = ROOT.dataset.loops || '1';
        const cs = getComputedStyle(ROOT);
        const tok = function (n, d) { return (cs.getPropertyValue(n) || '').trim() || d; };
        const c = { bg: tok('--ext-bg', '#0B2A3A'), fg: tok('--ext-fg', '#FFFFFF'), hi: tok('--ext-hi', '#13B8D0'), ink: tok('--ext-ink', '#0B2A3A') };
        const MISS = {}; (ROOT.dataset.miss || '').split('|').forEach(function (s) { const k = s.split(':'); if (k[0]) MISS[k[0]] = k[1] || ''; });
        /* ===== text-motion-40 code/_header.js（原作；只改 TL 一行）===== */
@@HEADER@@
        /* 缺字 fallback：該字體缺咥要顯示嘅字，成段改用品牌中文字體（同粗度），唔混兩款 */
        const BRAND = "'ExtBrand';font-weight:900";
        function FF(key, text) { const m = MISS[key] || ''; for (const ch of String(text)) { if (m.indexOf(ch) >= 0) return BRAND; } return F[key]; }
        /* ===== 原作 effect：@@CODE@@ ===== */
@@EFFECT@@
        const stage = ROOT.querySelector('.stage'), panel = ROOT.querySelector('.panel');
        const TOP = parseFloat(ROOT.querySelector('.pos').textContent);
        if (TOP) panel.style.top = TOP + 'px';
        panel.style.background = c.bg;
        const et = effect(stage, c);                       /* 原作回傳 paused timeline；由下面主時間線 seek，唔自己播 */
        const FREEZE = ROOT.dataset.freeze !== undefined ? +ROOT.dataset.freeze : (et.freeze !== undefined ? et.freeze : @@FREEZE@@);   /* effect 可設 tl.freeze＝建議凍結秒數 */
        const tl = gsap.timeline({ paused: true });
        const t0 = CUES.length ? Math.max(0, CUES[0] - 0.25) : 0.05;
        const CYCLE = 2;                                   /* 原作一個循環 2 秒 */
        const nLoops = LOOPS === 'auto' ? Math.max(1, Math.round((DUR - 0.4 - t0) * SPEED / CYCLE)) : Math.max(1, +LOOPS || 1);
        tl.fromTo(panel, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.2, ease: 'power2.out' }, Math.max(0, t0 - 0.05));
        if (nLoops === 1) {
          const to = FREEZE > 0 ? FREEZE : CYCLE;
          tl.add(et.tweenFromTo(0, to, { duration: to / SPEED, ease: 'none' }), t0);
        } else {
          for (let k = 0; k < nLoops; k++) tl.add(et.tweenFromTo(0, CYCLE, { duration: CYCLE / SPEED, ease: 'none' }), t0 + k * CYCLE / SPEED);
        }
        tl.to(panel, { autoAlpha: 0, y: 20, duration: 0.3, ease: 'power2.in' }, DUR - 0.32).set({}, {}, 7);
        window.__timelines["@@NAME@@"] = tl;
      })();
    </script>
  </body>
</html>
'''

def indent(src, n=8):
    return "\n".join((" " * n + l if l.strip() else l) for l in src.rstrip().split("\n"))

def build_card(eid, style="kallaway", scale=2.0, top=1010, freeze=0, force=False):
    """產生 styles/<style>/cards-9x16/<style>.x.ext<編號>.html，登記 style.json／portrait.json（未驗證）。回傳報告。"""
    E = load(); e = eff(E, eid); eid = e["id"]
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sd = os.path.join(root, "styles", style)
    if not os.path.isfile(os.path.join(sd, "style.json")): sys.exit(f"冇風格包 {style}")
    cid, name = f"{style}.x.ext{eid}", f"x-ext{eid}"
    rel = f"cards-9x16/{cid}.html"; dst = os.path.join(sd, rel)
    if os.path.exists(dst) and not force: sys.exit(f"✗ 已經有 {rel}（--force 覆蓋）")
    cf = code_file(eid); src = open(cf, encoding="utf-8").read(); hdr = open(os.path.join(TM, "code", "_header.js"), encoding="utf-8").read()
    if HEADER_TL not in hdr: print("! _header.js 嘅 TL() 同預期唔同，請人手檢查 repeat")
    hdr = hdr.replace(HEADER_TL, HEADER_TL_NEW)
    body = "\n".join(l for l in src.split("\n") if not l.startswith("//"))     # 原作頭幾行註解已搬去卡頭
    info = scan(src, scale); keys = info["fonts"]
    ff = [f"      @font-face {{ font-family: '{FAM[k]}'; src: url(assets/fonts/{FKEY[k]}); {'font-weight: 900; ' if k == 'zen' else ''}font-display: block; }}" for k in keys]
    ff.append("      @font-face { font-family: 'ExtBrand'; src: url(assets/fonts/sans900.woff2) format('woff2'); font-weight: 900; font-display: block; }  /* 缺字 fallback：Noto Sans TC 900 子集 */")
    warn = []
    if info["random"]: warn.append("原作有 Math.random：要改 rng(seed)")
    if info["timers"]: warn.append("有計時器 " + "/".join(info["timers"]) + "：HyperFrames 要可 seek，需改")
    if info["repeat"]: warn.append("effect 內部有 " + ", ".join(info["repeat"]) + "：確認唔會自己重複播")
    if e.get("caution") or eid in WARN: warn.append("⚠ " + (e.get("caution") or "EFFECTS.md 標 ⚠：冇睇分格圖唔准用"))
    small = "；".join(f"{a:g}px→{b:g}px" for a, b in info["small"])
    html_ = CARD
    for k, v in {"ID": eid, "EN": e["name_en"], "ZH": e["name_zh"], "DATE": datetime.date.today().isoformat(), "CODE": os.path.basename(cf),
                 "SC": f"{scale:g}", "DEMO": "、".join(info["demo"]) or "（搵程式碼入面嘅示範字）", "SMALL": ("目前 <76px：" + small) if small else "目前字級全部 ≥76px。",
                 "FREEZE": f"{freeze:g}", "STRIP": os.path.basename(e["strip"]), "CARD": cid, "WARN": ("警告：" + "；".join(warn)) if warn else "",
                 "FONTFACES": "\n".join(ff), "NAME": name, "TOP": str(top), "PANELW": f"{round(487 * scale)}", "PANELH": f"{round(160 * scale)}",
                 "HEADER": indent(hdr), "EFFECT": indent(body)}.items():
        html_ = html_.replace(f"@@{k}@@", v)
    os.makedirs(os.path.dirname(dst), exist_ok=True); open(dst, "w", encoding="utf-8").write(html_)
    # 登記
    sj, pj = os.path.join(sd, "style.json"), os.path.join(sd, "portrait.json")
    S = json.load(open(sj, encoding="utf-8")); P = json.load(open(pj, encoding="utf-8")) if os.path.exists(pj) else {}
    S["cards"] = [c for c in S["cards"] if c["id"] != cid]
    S["cards"].append({"id": cid, "tier": "tier2", "purpose": "ext", "treatment": f"text-motion-40#{eid}", "file": rel, "slots": [{"name": "top"}],
                       "duration": {"min": 2, "max": 10}, "custom": f"外部效果卡：text-motion-40 #{eid} {e['name_en']}（原作程式碼做起點）"})
    P[cid] = {"file": rel, "verified": False, "note": "外部效果卡起點，未換字／未對比分格圖", "source": f"text-motion-40#{eid}", "ext": {"id": eid, "fonts": keys}}
    json.dump(S, open(sj, "w", encoding="utf-8"), ensure_ascii=False, indent=1); json.dump(P, open(pj, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"✓ {rel}（卡 id {cid}）")
    print(f"  原作字體：{', '.join(FAM[k] for k in keys) or '—'}；舞台放大 {scale:g} 倍 → panel {round(487*scale)}×{round(160*scale)}px，top {top}")
    print(f"  示範字（要換）：{' / '.join(info['demo']) or '—'}")
    print(f"  字級（舞台 px → 放大後）：{', '.join(f'{a:g}→{b:g}' for a, b in info['sizes'])}" + (f"　✗ 低於 {MIN_FX_PX}px：{small}" if small else "　✓ 全部 ≥76px"))
    for w in warn: print("  !", w)
    return cid


if __name__ == "__main__":
    CMDS = {"list": cmd_list, "show": cmd_show, "table": cmd_table, "fontcheck": cmd_fontcheck, "brandfont": cmd_brandfont}
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS: sys.exit(__doc__)
    CMDS[sys.argv[1]](sys.argv[2:])
