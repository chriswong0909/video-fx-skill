#!/usr/bin/env python3
"""doctor2 full v3：所有畫面字由逐字時間計出（字對聲），同時輸出 manifest 俾 QA 用。"""
import json, re
END = 80.3
CS = json.load(open('chars.json'))
STREAM = ''.join(c['c'] for c in CS)

def find(text, after=0.0):
    """喺校正轉錄搵 text（去標點），回傳 (start,end)；搵唔到就 raise。"""
    t = re.sub(r'[，。、,.!?？！\s・+＋]', '', text)
    i0 = next(i for i, c in enumerate(CS) if c['s'] >= after - 0.01)
    k = STREAM.find(t, i0)
    if k < 0:
        raise SystemExit(f'字對聲失敗：「{text}」喺 {after}s 之後搵唔到')
    return CS[k]['s'], CS[k + len(t) - 1]['e']

# ---------- 字幕（每句 ≤10 字，時間全部由轉錄計）----------
PH = ["如果以前行樓梯沒問題", "@HOOK", "便要小心", "有機會可能", "心臟泵血功能下降", "影響心臟供血", "令到氣喘",
      "如果伴隨症狀", "例如腳腫", "睡平時氣喘", "有機會是心衰竭的初期", "有些人以為自己氣喘", "是因為體能下降",
      "其實如果是因為", "心臟功能衰退而氣喘", "再做運動", "可能會令到情況惡化", "@CARD1",
      "發生這些情況", "應該盡早找醫生", "做詳細檢查", "年紀大了", "心臟退化是正常的過程", "但這些不是單純看年紀",
      "你的生活習慣", "血管健康和", "新陳代謝情況", "都會影響退化的速度", "其實有些長者", "可能走一兩層樓梯", "便氣喘",
      "亦有些長者可以慢跑", "他們的分別當然是在於", "他們有沒有控制體重", "有沒有控制血壓、血糖", "如果他們配合",
      "生活習慣改善", "飲食改善和藥物", "當然可以減慢心臟退化", "如果病情是有需要的話", "現在醫學上有些藥物", "@CARD2",
      "對心臟、腎臟", "和新陳代謝的控制", "都有幫助"]
SKIP = {"@HOOK": "現在行一層樓梯便氣喘", "@CARD1": "因為氣喘有機會可能是心臟衰竭心律不正又或者心血管收窄",
        "@CARD2": "例如GLP-1受體促效劑和SGLT-2抑制劑他們除了控制血糖控制體重之外"}
spans, cur = [], 0.0
for p in PH:
    s, e = find(SKIP.get(p, p), cur)
    spans.append([p, s, e]); cur = e - 0.05
CAPS = []
for i, (p, s, e) in enumerate(spans):
    if p.startswith('@'): continue
    nxt = spans[i + 1][1] if i + 1 < len(spans) else END
    nxtcard = i + 1 < len(spans) and spans[i + 1][0].startswith('@')
    end = nxt if (nxt - e < 0.6 and not nxtcard) else min(e + 0.3, nxt)
    CAPS.append([p, round(s, 2), round(min(end, END), 2)])

def at(text, after=0.0): return round(find(text, after)[0], 2)

# ---------- 特效字（全部要喺講嗰刻出，字要係講過嘅字）----------
M = []   # manifest

# ================= v4：跟 Healthy Days 動態系統卡（brands/healthy-days/motion-system.md）=================
M = []
def beat(t):
    return 'hook' if t < 3.4 else 'setup' if t < 19 else 'tension' if t < 32.5 else 'turn' if t < 46 else 'proof' if t < 62.5 else 'payoff'
def add(id, kind, text, s, e, comp, enter, state='', spoken=True):
    M.append(dict(id=id, kind=kind, text=text, start=round(s, 2), end=round(e, 2), spoken=spoken, comp=comp, state=state, enter=enter, beat=beat(s)))

T_HOOK1, T_HOOK2 = at("行一層", 1.5), at("氣喘", 2.5)
add('hook', 'hook', '行一層便氣喘？', T_HOOK1, 3.4, 'hook', '撞入（品牌開場例外）')
add('tag', 'nametag', '心臟科專科醫生 江振昌', 3.9, 7.2, 'nametag', '向上浮入', spoken=False)

IMGS = [('i1', 'img_ankle.jpg', at('例如', 11), at('睡平', 12.5), [('腳腫', at('腳腫', 11))]),
        ('i2', 'img_bed.jpg', at('睡平', 12.5), at('有機會是', 14), [('睡平時氣喘', at('睡平', 12.5))]),
        ('i3', 'img_stairs.jpg', at('長者', 47), at('長者', 50), [('一兩層便氣喘', at('一兩層', 48))]),
        ('i4', 'img_jog.jpg', at('長者', 50), at('他們', 52), [('可以慢跑', at('可以慢跑', 50))]),
        ('i5', 'img_meal.jpg', at('配合', 58), at('當然', 62), [('生活', at('生活習慣改善', 58)), ('・飲食', at('飲食', 60)), ('・藥物', at('藥物', 61))])]
C1 = (at('因為氣喘有機會', 26), at('發生這些', 32))
C1ROWS = [('心臟衰竭', at('心臟衰竭', 28)), ('心律不正', at('心律不正', 29)), ('心血管收窄', at('心血管收窄', 31))]
C2 = (at('例如', 68), at('對心臟', 76))
C2ROWS = [('m1', 'GLP-1 受體促效劑', at('GLP', 68)), ('m2', 'SGLT-2 抑制劑', at('SGLT', 70)), ('b1', '控血糖', at('控制血糖', 73.5)), ('b2', '控體重', at('控制體重', 74.5))]
T_CROSS = at('其實', 20)

# ---------- 主角元素 #hero：每個「字組」= (id, 狀態, 字/子標籤, 出現秒, 填色) ----------
BLUE, GREEN = '#2f68a8', '#1f9d6b'
GROUPS = []   # dict(gid, state, parts=[(id,text,t)], t, fill, kind, spoken)
def grp(gid, state, parts, fill=BLUE, kind='imgtag', spoken=True): GROUPS.append(dict(gid=gid, state=state, parts=parts, t=parts[0][2], fill=fill, kind=kind, spoken=spoken))
grp('hg_i1', 'T', [('i1_l0', '腳腫', IMGS[0][4][0][1])])
grp('hg_i2', 'T', [('i2_l0', '睡平時氣喘', IMGS[1][4][0][1])])
grp('hg_k3', 'K', [('k3', '體能下降？', at('體能', 19))], kind='keyword')
grp('hg_c1', 'T', [('c1t', '3 個心臟問題', C1[0] + 0.1)], kind='cardtitle', spoken=False)
grp('hg_k5', 'K', [('k5', '盡早檢查', at('盡早', 33))], fill=GREEN, kind='keyword')
grp('hg_k6', 'K', [('k6', '不單看年紀', at('不是', 39))], kind='keyword')
grp('hg_i3', 'T', [('i3_l0', '一兩層便氣喘', IMGS[2][4][0][1])])
grp('hg_i4', 'T', [('i4_l0', '可以慢跑', IMGS[3][4][0][1])])
grp('hg_i5', 'T', [(f'i5_l{j}', t, ts) for j, (t, ts) in enumerate(IMGS[4][4])])
grp('hg_c2', 'T', [('c2t', '兩類藥物', C2[0] + 0.1)], kind='cardtitle', spoken=False)
grp('hg_k10', 'K', [('k10', '心臟・腎臟', at('心臟腎臟', 76))], kind='keyword')
# 出現窗口（窗口內連續使用 → 變形／換字）
WIN = [('hg_i1', 'hg_i2', IMGS[1][3]), ('hg_k3', 'hg_k3', 23.4), ('hg_c1', 'hg_c1', C1[1]), ('hg_k5', 'hg_k5', 36.4), ('hg_k6', 'hg_k6', 42.2),
       ('hg_i3', 'hg_i4', IMGS[3][3]), ('hg_i5', 'hg_i5', IMGS[4][3]), ('hg_c2', 'hg_k10', END)]
# 相隔 < 1 秒先變形；1 秒以上退場再入（唔好為咗變形而令舊字喺講者身上停留）
for a, b in zip(WIN, WIN[1:]): assert GROUPS[[g['gid'] for g in GROUPS].index(b[0])]['parts'][0][2] - a[2] >= 1.0, (a, b)
FS = {'T': 64, 'K': 104}
def em(t): return sum(1.0 if re.match(r'[　-鿿＀-￯]', c) else 0.3 if c == ' ' else 0.6 for c in t)
def width(state, text): return round(FS[state] * (2.9 + em(text)))
gi = {g['gid']: i for i, g in enumerate(GROUPS)}
for w0, w1, wend in WIN:
    seq = GROUPS[gi[w0]:gi[w1] + 1]
    for j, g in enumerate(seq):
        g['end'] = seq[j + 1]['t'] if j + 1 < len(seq) else wend
        full = ''.join(p[1] for p in g['parts'])
        g['w'] = [width(g['state'], ''.join(p[1] for p in g['parts'][:k + 1])) for k in range(len(g['parts']))]
        g['first'] = j == 0; g['last'] = j + 1 == len(seq); g['wend'] = wend
        for k, (pid, text, ts) in enumerate(g['parts']):
            enter = ('由左邊伸出' if g['state'] == 'T' else '向上浮入') if (j == 0 and k == 0) else ('變形' if k == 0 else '膠囊伸長')
            add(pid, g['kind'], text.lstrip('・'), ts, g['end'], 'hero', enter, state=g['state'], spoken=g['spoken'])

# ---------- 其他零件 ----------
SIDES = [([('生活習慣', at('生活習慣', 41)), ('血管健康', at('血管健康', 42)), ('新陳代謝', at('新陳代謝', 43))], at('其實有些長者', 46)),
         ([('體重', at('體重', 54)), ('血壓', at('血壓', 56)), ('血糖', at('血糖', 56.8))], at('如果他們配合', 57))]
for g, (items, end) in enumerate(SIDES):
    for j, (t, ts) in enumerate(items): add(f's{g}_{j}', 'label', t, ts, end, 'chip', '由右邊滑入')
for j, (t, ts) in enumerate(C1ROWS): add(f'g{j+1}', 'cardtext', t, ts, C1[1], 'row', '向上浮入')
for id, t, ts in C2ROWS: add(id, 'cardtext', t, ts, C2[1], 'row', '向上浮入')
for i, (t, s, e) in enumerate(CAPS): add(f'cap{i}', 'caption', t, s, e, 'caption', '硬切')

CAM = [(0, 1.35, 1.4, 3.4), (3.4, None, 1.0, 3.85), (3.85, 1.0, 1.0, at('有機會可能', 4)), (at('有機會可能', 4), None, 1.3, 6.4),
       (6.4, 1.3, 1.33, at('如果伴隨', 9)), (at('如果伴隨', 9), 1.0, 1.03, at('有些人', 17)), (at('有些人', 17), 1.3, 1.34, C1[0]),
       (C1[1], 1.0, 1.02, at('年紀大了', 36)), (at('年紀大了', 36), 1.3, 1.34, at('其實有些長者', 46)),
       (at('其實有些長者', 46), 1.0, 1.03, at('如果他們配合', 57)), (at('如果他們配合', 57), 1.3, 1.34, C2[0]), (C2[1], 1.0, 1.02, END)]

# ---------- 聲效：跟系統卡嘅聲效語言（動作 → 固定聲）----------
EV = []
def ev(t, sfx, vol, why): EV.append(dict(t=round(t, 3), sfx=sfx, vol=vol, why=why))
ev(0.05, 'SFX-015', 0.5, '開場心跳（品牌例外）')
ev(T_HOOK1 + 0.22, 'SFX-011', 0.28, '「行一層」撞入（品牌例外）')
ev(T_HOOK2 + 0.22, 'SFX-011', 0.45, '「便氣喘？」撞入＋紅閃（品牌例外）')
ev(3.70, 'SFX-001', 0.30, '拉返闊鏡（鏡頭）')
ev(3.9 + 0.3, 'SFX-005', 0.30, '名牌浮入')
for g in GROUPS:
    if g['fill'] != BLUE: pass   # 正面綠色版：由 SFX-009 代替滑入聲（一個動作一個聲）
    elif g['first']: ev(g['t'] + 0.3, 'SFX-014', 0.32, f"藍膠囊伸出「{g['parts'][0][1]}」")
    elif g['state'] != GROUPS[gi[g['gid']] - 1]['state']: ev(g['t'] + 0.3, 'SFX-014', 0.3, f"藍膠囊變形 →「{g['parts'][0][1]}」")
    for pid, text, ts in g['parts'][1:]: ev(ts + 0.2, 'SFX-005', 0.25, f'膠囊伸長「{text}」')
ev(T_CROSS + 0.2, 'SFX-010', 0.32, '紅交叉（錯誤觀念）')
ev(at('盡早', 33) + 0.3, 'SFX-009', 0.3, '綠色正面「盡早檢查」')
for items, end in SIDES: ev(items[0][1] + 0.3, 'SFX-005', 0.25, f'白膠囊「{items[0][0]}」滑入')
for t, ts in C1ROWS: ev(ts + 0.3, 'SFX-005', 0.28, f'卡片行「{t}」浮入')
for id, t, ts in C2ROWS: ev(ts + 0.3, 'SFX-005', 0.28, f'卡片行「{t}」浮入')
EV.sort(key=lambda e: e['t'])
json.dump(EV, open('sfx-events.json', 'w'), ensure_ascii=False, indent=0)

# ---------- HTML ----------
CROSS = '<svg class="cr" viewBox="0 0 54 54"><path d="M19 4h16v15h15v16H35v15H19V35H4V19h15z" fill="#ffffff"/></svg>'
def part_html(pid, text):
    if pid == 'k3': return '<span id="k3"><span class="x">體能下降<i id="xa"></i><i id="xb"></i></span>？</span>'
    return f'<span id="{pid}">{text}</span>'
hero_html = '<div id="hero">' + CROSS + '<div class="tx">' + ''.join(
    f'<div class="g" id="{g["gid"]}">' + ''.join(part_html(p, t) for p, t, ts in g['parts']) + '</div>' for g in GROUPS) + '</div></div>'
img_html = ''.join(f'<div class="imgc clip" id="{id}" data-start="{s}" data-duration="{round(e-s,2)}" data-track-index="{5+n}"><img src="assets/{f}" alt=""></div>'
                   for n, (id, f, s, e, labs) in enumerate(IMGS))
side_html = ''.join(f'<div class="side" id="sg{g}">' + ''.join(f'<span id="s{g}_{j}">{t}</span>' for j, (t, ts) in enumerate(items)) + '</div>' for g, (items, end) in enumerate(SIDES))
D = dict(END=END, CAPS=CAPS, IMGS=IMGS, SIDES=SIDES, CAM=CAM, C1=C1, C1ROWS=C1ROWS, C2=C2, C2ROWS=C2ROWS,
         T_HOOK1=T_HOOK1, T_HOOK2=T_HOOK2, T_CROSS=T_CROSS, GROUPS=GROUPS, FS=FS)
html = open('template4.html').read()
html = html.replace('/*__DATA__*/', 'const D=' + json.dumps(D, ensure_ascii=False) + ';')
html = html.replace('<!--HERO-->', hero_html).replace('<!--IMGS-->', img_html).replace('<!--SIDES-->', side_html)
html = html.replace('__C1S__', str(C1[0])).replace('__C1D__', str(round(C1[1] - C1[0], 2))).replace('__C2S__', str(C2[0])).replace('__C2D__', str(round(C2[1] - C2[0], 2)))
html = html.replace('<!--MANIFEST-->', '<script type="application/json" id="fx-manifest">' + json.dumps(M, ensure_ascii=False) + '</script>')
open('index.html', 'w').write(html)
json.dump(M, open('manifest.json', 'w'), ensure_ascii=False, indent=0)
print('ok', len(M), 'elements;', len(CAPS), 'captions;', len(GROUPS), 'hero groups')
for g in GROUPS: print(f"  {g['gid']:7} {g['state']} {g['t']:6.2f}–{g['end']:6.2f} w={g['w']} first={g['first']} last={g['last']}")
