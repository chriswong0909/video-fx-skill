#!/usr/bin/env node
// usage: node scripts/build-storyboard.mjs storyboards/<name>.json  -> storyboards/<name>.html (Artifact fragment)
// Cheap preview: uses effect-library preview stills, no rendering.
import fs from 'node:fs'; import path from 'node:path'; import { fileURLToPath } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const inFile = path.resolve(process.argv[2]); const sb = JSON.parse(fs.readFileSync(inFile, 'utf8'));
const reg = JSON.parse(fs.readFileSync(path.join(root, 'registry.json'), 'utf8')); const byId = Object.fromEntries(reg.effects.map(e => [e.id, e]));
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const sById = Object.fromEntries((reg.sounds || []).map(x => [x.id, x]));
const sAudio = id => { const x = sById[id]; if (!x) return ''; const f = path.join(root, x.path, 'sound.mp3'); return fs.existsSync(f) ? 'data:audio/mpeg;base64,' + fs.readFileSync(f).toString('base64') : ''; };
const thumb = id => { const e = byId[id]; if (!e) return ''; const f = path.join(root, e.path, 'preview.jpg'); return fs.existsSync(f) ? 'data:image/jpeg;base64,' + fs.readFileSync(f).toString('base64') : ''; };
const fmt = t => { t = +t; const m = Math.floor(t / 60); return `${m}:${(t - m * 60).toFixed(1).padStart(4, '0')}`; };
const SRC = { code: '代碼自製', higgsfield: 'Higgsfield', canva: 'Canva', client: '客戶提供', footage: '原片', stock: '素材庫' };
const BEAT = { hook: 'Hook', setup: '鋪陳', tension: '張力', proof: '證據', turn: '轉折', payoff: '收結' };
let total = 0; const assetRows = [];
const shots = sb.shots.map((s, i) => {
  (s.assets || []).forEach(a => { total += +(a.credits || 0); assetRows.push({ shot: i + 1, ...a }); });
  const fx = (s.fx || []).map(id => `<figure class="fx"><img src="${thumb(id)}" alt=""><figcaption><b>${esc(id)}</b> ${esc(byId[id]?.name || '未入庫')}</figcaption></figure>`).join('');
  return `<article class="shot"><div class="tc">${String(i + 1).padStart(2, '0')}<span>${fmt(s.t0)}–${fmt(s.t1)}</span></div>
  <div class="main">${s.beat ? `<p class="bt"><span class="beat ${esc(s.beat)}">${esc(BEAT[s.beat] || s.beat)}</span>${s.cam ? `<span class="cam">機位 ${esc(s.cam)}</span>` : ''}${s.caption ? `<span class="cam">字幕：${esc(s.caption)}</span>` : ''}</p>` : ''}<p class="line">「${esc(s.line)}」</p><p class="vis">${esc(s.visual)}</p>${s.holdReason ? `<p class="note">停留原因：${esc(s.holdReason)}</p>` : ''}${s.notes ? `<p class="note">${esc(s.notes)}</p>` : ''}
  ${(s.sfx || []).length ? `<p class="sfx">聲效：${s.sfx.map(c => `<button class="sb" onclick="new Audio(this.dataset.a).play()" data-a="${sAudio(c.sfx)}">▶ ${esc(c.sfx)} ${esc(sById[c.sfx]?.name || '未入庫')} <em>@${(+c.t).toFixed(1)}s</em></button>`).join(' ')}</p>` : ''}
  ${(s.assets || []).length ? `<ul class="as">${s.assets.map(a => `<li><span class="src ${esc(a.source)}">${esc(SRC[a.source] || a.source)}</span>${esc(a.what)}${a.credits ? ` <em>${a.credits} credits</em>` : ''}</li>`).join('')}</ul>` : ''}</div>
  <div class="fxs">${fx}</div></article>`;
}).join('\n');
const html = `<title>${esc(sb.title)} 分鏡</title>
<style>
:root{--bg:#eef0f2;--sf:#fff;--ink:#16191d;--mu:#5b636d;--ln:#d5d9df;--ac:#d8452b;--hf:#6d4aff;--cv:#00a3a3;--cl:#b7791f;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#121417;--sf:#1b1e22;--ink:#e8ebee;--mu:#9aa2ac;--ln:#2d3239;--ac:#ff6a4d;--hf:#9b85ff;--cv:#2cc7c7;--cl:#e0a84a;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#121417;--sf:#1b1e22;--ink:#e8ebee;--mu:#9aa2ac;--ln:#2d3239;--ac:#ff6a4d;--hf:#9b85ff;--cv:#2cc7c7;--cl:#e0a84a;color-scheme:dark}
*{box-sizing:border-box}body{background:var(--bg);color:var(--ink);font-family:"Noto Sans TC",system-ui,-apple-system,"PingFang TC",sans-serif;font-size:15px;line-height:1.55;padding-inline:clamp(16px,4vw,44px);padding-block:26px 60px}
.w{max-width:1100px;margin:0 auto;display:flex;flex-direction:column;gap:18px}h1{margin:0;font-size:clamp(24px,3.4vw,34px);font-weight:900}
.meta{display:flex;flex-wrap:wrap;gap:8px 22px;color:var(--mu);font-size:13.5px}.meta b{color:var(--ink)}
.shot{display:grid;grid-template-columns:84px minmax(0,1fr) minmax(0,300px);gap:16px;background:var(--sf);border:1px solid var(--ln);border-radius:10px;padding:14px}
.tc{font:500 26px/1 ui-monospace,Menlo,monospace}.tc span{display:block;font-size:12px;color:var(--mu);margin-top:6px}
.line{margin:0;font-weight:700}.vis{margin:6px 0 0}.note{margin:6px 0 0;color:var(--mu);font-size:13.5px}
.as{margin:8px 0 0;padding:0;list-style:none;display:flex;flex-direction:column;gap:4px;font-size:13.5px}.as em{color:var(--mu);font-style:normal;font-family:ui-monospace,monospace;font-size:12px}
.src{display:inline-block;font-size:11.5px;border-radius:4px;padding:1px 7px;margin-right:8px;border:1px solid var(--ln)}.src.higgsfield{color:var(--hf);border-color:var(--hf)}.src.canva{color:var(--cv);border-color:var(--cv)}.src.client{color:var(--cl);border-color:var(--cl)}
.sfx{margin:6px 0 0;font-size:13px;display:flex;flex-wrap:wrap;gap:6px;align-items:center}.sb{font:inherit;font-size:12.5px;border:1px solid #c2410c55;background:#c2410c14;color:inherit;border-radius:6px;padding:3px 8px;cursor:pointer}.sb em{font-style:normal;opacity:.65}
.fxs{display:flex;gap:8px;flex-wrap:wrap}.fx{margin:0;width:92px}.fx img{width:92px;aspect-ratio:9/16;object-fit:cover;border-radius:6px;background:#111;display:block}.fx figcaption{font-size:11.5px;color:var(--mu);line-height:1.3;margin-top:4px}.fx b{color:var(--ink);font-family:ui-monospace,monospace;font-weight:500}
table{width:100%;border-collapse:collapse;font-size:13.5px}th,td{text-align:left;padding:7px 8px;border-bottom:1px solid var(--ln);vertical-align:top}th{color:var(--mu);font-weight:500}td.n{font-family:ui-monospace,monospace;text-align:right}.tw{overflow-x:auto;background:var(--sf);border:1px solid var(--ln);border-radius:10px;padding:6px 10px}
.bt{margin:0 0 6px;display:flex;flex-wrap:wrap;gap:6px}.beat,.cam{font-size:12px;border-radius:999px;padding:2px 9px;border:1px solid var(--ln);color:var(--mu)}.beat{color:#fff;border:0;background:#5b636d}.beat.hook{background:#d8452b}.beat.turn{background:#0b7fa8}.beat.tension{background:#b3261e}.beat.proof{background:#3d5a80}.beat.payoff{background:#1f8a5b}
.tr td:first-child{white-space:nowrap;color:var(--mu)}.gimg{width:100%;border-radius:8px;display:block}
.gate{border:1px solid var(--ac);border-radius:10px;padding:12px 16px;background:var(--sf)}
@media (max-width:760px){.shot{grid-template-columns:1fr}.tc span{display:inline;margin-left:10px}}
</style>
<div class="w"><header><h1>${esc(sb.title)}</h1><div class="meta"><span>素材 <b>${esc(sb.source || '')}</b></span><span>長度 <b>${esc(sb.duration || '')}</b></span><span>比例 <b>${esc(sb.ratio || '')}</b></span><span>風格 <b>${esc(sb.style || '')}</b></span>${sb.preset ? `<span>風格預設 <b>${esc(sb.preset)}</b></span>` : ''}${sb.grade ? `<span>調色 <b>${esc(sb.grade)}</b></span>` : ''}<span>鏡頭 <b>${sb.shots.length}</b></span></div></header>
${sb.treatment ? `<h2 style="margin:6px 0 0;font-size:19px">Treatment（已確認）</h2><div class="tw"><table class="tr">${Object.entries(sb.treatment).map(([k, v]) => `<tr><td>${esc(k)}</td><td>${esc(v)}</td></tr>`).join('')}</table></div>` : ''}
${sb.grade_image && fs.existsSync(path.resolve(path.dirname(inFile), sb.grade_image)) ? `<h2 style="margin:6px 0 0;font-size:19px">調色對比</h2><img class="gimg" alt="調色對比" src="data:image/jpeg;base64,${fs.readFileSync(path.resolve(path.dirname(inFile), sb.grade_image)).toString('base64')}">` : ''}
<h2 style="margin:6px 0 0;font-size:19px">分鏡</h2>
${shots}
<h2 style="margin:10px 0 0;font-size:20px">素材清單</h2><div class="tw"><table><thead><tr><th>鏡頭</th><th>來源</th><th>素材</th><th>生成描述</th><th>credits</th></tr></thead><tbody>
${assetRows.map(a => `<tr><td>${a.shot}</td><td><span class="src ${esc(a.source)}">${esc(SRC[a.source] || a.source)}</span></td><td>${esc(a.what)}</td><td>${esc(a.prompt || '—')}</td><td class="n">${a.credits ?? '—'}</td></tr>`).join('')}
<tr><td colspan="4"><b>預計總額</b></td><td class="n"><b>${total || '—'}</b></td></tr></tbody></table></div>
<div class="gate"><b>下一步</b>：確認分鏡同素材清單 → 生成素材（會用 credits）→ 出草稿（低畫質）→ 確認 → 出正式版。</div></div>`;
const out = inFile.replace(/\.json$/, '.html'); fs.writeFileSync(out, html); console.log(`storyboard -> ${path.relative(root, out)} (${sb.shots.length} shots, ${total} credits)`);
