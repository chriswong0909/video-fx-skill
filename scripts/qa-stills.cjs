// qa-stills.cjs — 逐個畫面字截圖 + 位置檢查（出血位、logo、置中）
// node qa-stills.cjs <project_dir> <frames_dir(每秒 10 格 f_0001.jpg…)> <out_dir>
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const [dir, framesDir, out] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
const SAFE = { x0: 52, x1: 1028, y0: 212, y1: 1556 }, LOGO = { x0: 742, y0: 228, x1: 1020, y1: 360 };
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(dir, 'index.html')); await p.waitForTimeout(1200);
  const M = await p.evaluate(() => JSON.parse(document.getElementById('fx-manifest').textContent));
  const fails = []; const shots = [];
  for (const x of M) {
    const t = Math.min(x.start + 0.6, x.end - 0.05);
    const f = path.resolve(framesDir, 'f_' + String(Math.round(t * 10) + 1).padStart(4, '0') + '.jpg');
    const sel = { c1t: '#card1 .ttag', c2t: '#card2 .ttag' }[x.id] || '#' + x.id;
    const r = await p.evaluate(([t, f, sel, kind]) => {
      const v = document.getElementById('vid'); v.style.background = `url(${f}) center/cover`; v.removeAttribute('src');
      document.querySelectorAll('.clip').forEach(c => { if (c.id === 'fx051') return; const a = +c.dataset.start, d = +c.dataset.duration; c.style.visibility = (t >= a && t < a + d) ? 'visible' : 'hidden'; /* 同 HyperFrames 一樣用 visibility 收 clip */ });
      window.__timelines.main.seek(t);
      let el = document.querySelector(sel); if (!el) return { missing: true };
      if (kind === 'caption' || kind === 'label') el = el.querySelector('span') || el;
      const q = el.getBoundingClientRect(); const st = getComputedStyle(el);
      // 字嘅實際範圍：用 Range 量文字
      const rg = document.createRange(); rg.selectNodeContents(el); const tr = rg.getBoundingClientRect();
      const bar = el.closest('.ttag'); const br = bar ? bar.getBoundingClientRect() : null;
      const it = (el.innerText || '').replace(/[^\u4e00-\u9fffA-Za-z0-9]/g, '');
      return { it, bar: br ? { x0: br.left, y0: br.top, x1: br.right, y1: br.bottom } : null, x0: q.left, y0: q.top, x1: q.right, y1: q.bottom, tx0: tr.left, tx1: tr.right, ty0: tr.top, ty1: tr.bottom, vis: st.visibility, op: +st.opacity };
    }, [t, f, sel, x.kind]);
    await p.waitForTimeout(80);
    const png = path.join(out, `${String(Math.round(t * 100)).padStart(5, '0')}_${x.id}.jpg`);
    await p.screenshot({ path: png, type: 'jpeg', quality: 80 }); shots.push(png);
    if (r.missing) { fails.push(`${x.id}「${x.text}」揾唔到元素`); continue; }
    const want = x.text.replace(/[^\u4e00-\u9fffA-Za-z0-9]/g, '');
    if (!['nametag'].includes(x.kind) && !r.it.includes(want)) fails.push(`${x.id}「${x.text}」文字冇顯示（畫面只見到「${r.it}」）`);
    if (r.vis !== 'visible' || r.op < 0.9) fails.push(`${x.id}「${x.text}」@${t.toFixed(2)}s 應該見到但 visibility=${r.vis} opacity=${r.op}`);
    const bx = x.kind === 'imgtag' || x.kind === 'cardtitle' ? { x0: r.tx0, x1: r.tx1, y0: r.ty0, y1: r.ty1 } : r;
    if (bx.x0 < SAFE.x0 - 1 || bx.x1 > SAFE.x1 + 1 || bx.y0 < SAFE.y0 - 1 || bx.y1 > SAFE.y1 + 1) fails.push(`${x.id}「${x.text}」出咗 IG 安全區 (${bx.x0 | 0},${bx.y0 | 0})-(${bx.x1 | 0},${bx.y1 | 0})`);
    if (!(bx.x1 < LOGO.x0 || bx.x0 > LOGO.x1 || bx.y1 < LOGO.y0 || bx.y0 > LOGO.y1)) fails.push(`${x.id}「${x.text}」撞到右上 logo`);
    if (r.bar && !(r.bar.x1 < LOGO.x0 || r.bar.x0 > LOGO.x1 || r.bar.y1 < LOGO.y0 || r.bar.y0 > LOGO.y1)) fails.push(`${x.id}「${x.text}」嘅 title bar 撞到 logo`);
    if (['caption', 'keyword', 'hook'].includes(x.kind)) { const cx = (r.tx0 + r.tx1) / 2; if (Math.abs(cx - 540) > 14) fails.push(`${x.id}「${x.text}」冇置中（中心 x=${cx | 0}）`); }
  }
  // 結束後 0.3 秒唔應該再見到
  for (const x of M) { const t = x.end + 0.3; if (t >= 80.2) continue;
    const sel = { c1t: '#card1 .ttag', c2t: '#card2 .ttag' }[x.id] || '#' + x.id;
    const still = await p.evaluate(([t, sel]) => {
      document.querySelectorAll('.clip').forEach(c => { if (c.id === 'fx051') return; const a = +c.dataset.start, d = +c.dataset.duration; c.style.visibility = (t >= a && t < a + d) ? 'visible' : 'hidden'; });
      window.__timelines.main.seek(t); const el = document.querySelector(sel); if (!el) return false;
      return [el, ...el.querySelectorAll('*')].some(n => { const s = getComputedStyle(n); if (s.visibility !== 'visible' || !n.getClientRects().length) return false;
        let o = 1, q = n; while (q && q !== document.body) { o *= +getComputedStyle(q).opacity; q = q.parentElement; } return o > 0.05 && (n.textContent || '').trim().length > 0 || (o > 0.05 && n.tagName === 'I'); });
    }, [t, sel]);
    if (still) fails.push(`${x.id}「${x.text}」應該 ${x.end}s 收，但 ${t.toFixed(2)}s 仲見到`);
  }
  await b.close();
  console.log(`截圖 ${shots.length} 張 → ${out}`); fails.forEach(f => console.log(' ✗', f));
  console.log(fails.length ? `✗ ${fails.length} 項位置問題` : '✓ 位置全過');
  process.exitCode = fails.length ? 1 : 0;
})();
