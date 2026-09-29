#!/usr/bin/env node
// check-style.mjs — 一致性檢查（出草稿前行）
// usage: node scripts/check-style.mjs <composition.html> [presets/SP-xxx-...]
// 檢查：字體 ≤ 2、色相 ≤ 4、緩動 ≤ 4、轉場 ≤ 2、效果白名單、中文唔用大楷／斜體、字級下限、確定性
import fs from 'node:fs'; import path from 'node:path'; import { fileURLToPath } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const [file, presetDir] = process.argv.slice(2);
if (!file) { console.log('usage: node scripts/check-style.mjs <composition.html> [presets/SP-xxx]'); process.exit(1); }
const html = fs.readFileSync(file, 'utf8');
const preset = presetDir ? JSON.parse(fs.readFileSync(path.join(presetDir, 'preset.json'), 'utf8')) : null;
const reg = fs.existsSync(path.join(root, 'registry.json')) ? JSON.parse(fs.readFileSync(path.join(root, 'registry.json'), 'utf8')) : { effects: [] };
const cat = Object.fromEntries(reg.effects.map(e => [e.id, e.category]));
const res = []; const add = (level, item, msg) => res.push({ level, item, msg });

// token 值（preset + composition 內 :root 定義）
const tokens = {};
if (preset) for (const [k, v] of Object.entries(preset.tokens)) tokens['--' + k.replace(/_/g, '-').replace(/^(bg|surface|text|accent|alert|positive|caption-box|caption-text)$/, 'c-$1')] = v;
for (const m of html.matchAll(/(--[a-z0-9-]+)\s*:\s*([^;}]+)/g)) tokens[m[1]] = m[2].trim();
const resolve = s => s.replace(/var\((--[a-z0-9-]+)\s*(?:,\s*([^()]*(?:\([^()]*\))?[^()]*))?\)/g, (_, n, d) => tokens[n] ?? d ?? '');

// 1) 字體
const GENERIC = /^(sans-serif|serif|monospace|system-ui|inherit|initial|cursive)$/i;
const fonts = new Set();
for (const m of html.matchAll(/font-family\s*:\s*([^;}]+)/g)) resolve(m[1]).split(',').map(s => s.trim().replace(/^['"]|['"]$/g, '')).filter(s => s && !GENERIC.test(s) && !s.startsWith('--')).slice(0, 1).forEach(f => fonts.add(f));
for (const m of html.matchAll(/font\s*:\s*[^;}]*?\d+px(?:\/[\d.]+)?\s+([^;}]+)/g)) { const f = resolve(m[1]).split(',')[0].trim().replace(/^['"]|['"]$/g, ''); if (f && !GENERIC.test(f)) fonts.add(f); }
for (const m of html.matchAll(/fontFamily\s*:\s*['"]([^'"]+)['"]/g)) fonts.add(m[1].split(',')[0].trim().replace(/^['"]|['"]$/g, ''));
add(fonts.size <= 2 ? 'ok' : 'fail', '字體', `${fonts.size} 款：${[...fonts].join('、') || '—'}（上限 2）`);

// 2) 色相
const hexes = new Set();
const src = resolve(html.replace(/<video[^>]*>/g, ''));
for (const m of src.matchAll(/#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b/g)) { let h = m[1]; if (h.length === 3) h = h.split('').map(c => c + c).join(''); hexes.add(h.toLowerCase()); }
for (const m of src.matchAll(/rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)/g)) hexes.add([m[1], m[2], m[3]].map(n => (+n).toString(16).padStart(2, '0')).join(''));
const hsl = h => { const [r, g, b] = [0, 2, 4].map(i => parseInt(h.slice(i, i + 2), 16) / 255); const mx = Math.max(r, g, b), mn = Math.min(r, g, b), l = (mx + mn) / 2, d = mx - mn;
  if (!d) return { h: 0, s: 0, l }; const s = d / (1 - Math.abs(2 * l - 1)); let hh = mx === r ? ((g - b) / d) % 6 : mx === g ? (b - r) / d + 2 : (r - g) / d + 4; return { h: (hh * 60 + 360) % 360, s, l }; };
const hues = []; const chroma = [...hexes].filter(h => { const c = hsl(h); return c.s > 0.18 && c.l > 0.1 && c.l < 0.93; });
for (const h of chroma) { const c = hsl(h).h; if (!hues.some(x => Math.min(Math.abs(x - c), 360 - Math.abs(x - c)) < 24)) hues.push(c); }
add(hues.length <= 4 ? 'ok' : 'fail', '色相', `${hues.length} 組（${chroma.map(h => '#' + h).join(' ')}）（上限 4，黑白灰唔計）`);
if (preset) { const allowed = ['accent', 'alert', 'positive', 'caption_box', 'bg', 'surface', 'text', 'caption_text'].map(k => (preset.tokens[k] || '').toLowerCase().replace('#', ''));
  const off = chroma.filter(h => !allowed.includes(h)); if (off.length) add('warn', '預設外顏色', off.map(h => '#' + h).join(' ') + ' —— 改用 var(--c-accent / --c-alert / --c-positive)'); }

// 3) 緩動
const eases = new Set();
for (const m of html.matchAll(/ease\s*:\s*(['"])([^'"]+)\1/g)) if (m[2] !== 'none') eases.add(m[2]);
for (const m of html.matchAll(/ease\s*:\s*EASE\.(\w+)/g)) eases.add(preset ? preset.tokens['ease_' + m[1]] || 'EASE.' + m[1] : 'EASE.' + m[1]);
add(eases.size <= 4 ? 'ok' : 'fail', '緩動', `${eases.size} 款：${[...eases].join('、') || '—'}（上限 4，none 唔計）`);

// 4) 效果、轉場、白名單
const used = [...new Set([...html.matchAll(/FX-\d{3}/g)].map(m => m[0]))];
const trans = used.filter(id => cat[id] === 'transition');
add(trans.length <= 2 ? 'ok' : 'fail', '轉場', `${trans.length} 款：${trans.join('、') || '—'}（上限 2）`);
const caps = used.filter(id => cat[id] === 'caption');
add(caps.length <= 1 ? 'ok' : 'fail', '字幕款式', `${caps.length} 款：${caps.join('、') || '—'}（全片只用一款）`);
if (preset) { const out = used.filter(id => !preset.effects.includes(id)); add(out.length ? 'warn' : 'ok', '白名單', out.length ? `${preset.id} 白名單以外：${out.join('、')} —— 分鏡要寫理由` : `全部喺 ${preset.id} 白名單`); }

// 5) 中文排版
if (/[一-鿿]/.test(html)) {
  if (/text-transform\s*:\s*uppercase/.test(html)) add('warn', '大楷', '有 text-transform:uppercase —— 中文字唔好用（只限英文標籤）');
  if (/font-style\s*:\s*italic/.test(html)) add('warn', '斜體', '有 font-style:italic —— 中文冇真斜體，會變假斜');
}
const small = [...html.matchAll(/font(?:-size)?\s*:[^;}]*?(\d+)px/g)].map(m => +m[1]).filter(n => n < 52);
if (small.length) add('warn', '字級', `有 ${small.length} 處細過 52px（${[...new Set(small)].join('、')}px）——手機睇唔清`);

// 6) 確定性
if (/Math\.random\s*\(/.test(html)) add('fail', '隨機', '用咗 Math.random() —— 改用 seeded mulberry32');
if (/repeat\s*:\s*-1/.test(html)) add('fail', '無限循環', 'repeat:-1 —— 改用固定次數');
if (!/tl\.to\(\{\}\s*,\s*\{\s*duration/.test(html)) add('warn', '時間軸墊底', "冇 tl.to({}, {duration: TOTAL}, 0) —— 結尾可能黑一格");

const icon = { ok: '✓', warn: '!', fail: '✗' };
console.log(`一致性檢查：${path.basename(file)}${preset ? '（' + preset.id + ' ' + preset.name + '）' : ''}`);
for (const r of res) console.log(` ${icon[r.level]} ${r.item}：${r.msg}`);
const fails = res.filter(r => r.level === 'fail').length, warns = res.filter(r => r.level === 'warn').length;
console.log(fails ? `\n✗ ${fails} 項唔過，改完先出草稿` : `\n✓ 通過（${warns} 項提示）`);
process.exitCode = fails ? 1 : 0;
