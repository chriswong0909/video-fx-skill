#!/usr/bin/env python3
"""外部效果來源（text-motion-40）查詢 + 出配對表。見 workflow/external-effects.md

  python3 tools/ext_effects.py list [--use 強調] [--cat IMPACT|FLOW|DEPTH|SWITCH|STYLE]   # 列款（⚠＝冇睇圖唔准用）
  python3 tools/ext_effects.py show 29                  # 提示詞、分格圖／短片路徑、注意
  python3 tools/ext_effects.py table matches.json out.html   # 出配對表（分格圖內嵌 base64），再用 Artifact 發佈

來源路徑：環境變數 TM40（預設 ~/Documents/GitHub/text-motion-40）。本機冇就用 GitHub MCP 讀 chriswong0909/text-motion-40。

matches.json：
{"project": "骨質疏鬆", "brand": "Healthy Days（Kallaway 淺色）",
 "items": [{"slot": "hook", "line": "原句", "t": "0:08",
            "cands": [{"id": "29", "why": "點解 match"}, {"id": "03", "why": "…"}]}],
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
                     f"<img alt='{html.escape(e['name_en'])} 分格圖' src='data:image/jpeg;base64,{b64}'></div>")
        h.append("</section>")
    if m.get("none_reason"):
        h.append(f"<p class='note'><b>一款都唔用：</b>{html.escape(m['none_reason'])}</p>")
    h.append("</main>")
    open(out, "w", encoding="utf-8").write("\n".join(h)); print("✓", out, os.path.getsize(out) // 1024, "KB")

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("list", "show", "table"): sys.exit(__doc__)
    {"list": cmd_list, "show": cmd_show, "table": cmd_table}[sys.argv[1]](sys.argv[2:])
