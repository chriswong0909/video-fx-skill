// qa-motion.cjs — 一致性檢查：實際時間軸有冇跟動態系統卡（緩動、時長、入場文法、顏色、零件）
// node scripts/qa-motion.cjs <project_dir/index.html> <motion-system.json>
// 讀 window.__timelines.main 每一個 tween + fx-manifest，超出系統卡 → ✗（唔准渲染）
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const [html, sysPath] = process.argv.slice(2);
if (!html || !sysPath) { console.log('usage: node scripts/qa-motion.cjs index.html motion-system.json'); process.exit(2); }
const SYS = JSON.parse(fs.readFileSync(sysPath, 'utf8'));
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(html)); await p.waitForTimeout(1000);
  const R = await p.evaluate((SYS) => {
    const tl = window.__timelines.main; const hero = SYS.hero ? document.querySelector(SYS.hero) : null;
    const exempt = el => el && el.nodeType === 1 && SYS.exempt.some(s => el.matches(s) || el.closest(s));
    const name = el => el.id ? '#' + el.id : (el.className && el.className.baseVal === undefined ? '.' + String(el.className).split(' ')[0] : el.tagName);
    const out = { tweens: [], issues: [] };
    for (const tw of tl.getChildren(true, true, false)) {
      const tg = tw.targets().filter(t => t && t.nodeType === 1);
      if (!tg.length || tg.every(exempt)) continue;
      const d = +tw.duration().toFixed(3); if (d === 0) continue;             // set
      const v = tw.vars; const ease = typeof v.ease === 'string' ? v.ease : (v.ease ? 'custom' : 'DEFAULT(power1.out)');
      const from = v.startAt || null; const keys = Object.keys(from || v).filter(k => !['ease', 'duration', 'immediateRender', 'overwrite', 'transformOrigin', 'startAt'].includes(k));
      const inHero = hero && tg.some(t => hero === t || hero.contains(t));
      let kind = 'other';
      if (ease === 'none' && d >= 1) kind = 'hold';
      else if (!from) {                                                         // .to()
        const k = Object.keys(v);
        if (inHero && k.some(x => ['left', 'top', 'width', 'fontSize', 'borderRadius', 'xPercent', 'backgroundColor'].includes(x))) kind = (v.opacity === 0 || (v.xPercent !== undefined && v.xPercent <= -100)) ? 'exit' : 'morph';
        else if (v.opacity === 0 || (typeof v.xPercent === 'number' && Math.abs(v.xPercent) >= 100)) kind = 'exit';
        else if (k.includes('x') && !k.includes('y')) kind = 'shake';
      } else {                                                                  // .fromTo() 入場
        if (inHero && (keys.includes('filter') || keys.join() === 'opacity')) kind = 'morph';
        else if (keys.includes('scaleX') || keys.includes('attr')) kind = 'draw';
        else if (keys.includes('xPercent') || keys.includes('x')) kind = 'slide-edge';
        else if (keys.includes('y')) kind = 'rise';
        else if (keys.includes('scale')) kind = 'scale';
        else if (keys.join() === 'opacity') kind = 'fade';
      }
      out.tweens.push({ el: tg.map(name).slice(0, 2).join(','), t: +tw.startTime().toFixed(2), d, ease, kind });
    }
    // 顏色：每個畫面字喺出現中段，量佢同子元素實際顏色
    const M = JSON.parse(document.getElementById('fx-manifest').textContent);
    const hex = c => { const m = c.match(/rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?/); if (!m || (m[4] !== undefined && +m[4] < 0.05)) return null; return '#' + [1, 2, 3].map(i => (+m[i] | 0).toString(16).padStart(2, '0')).join(''); };
    const colors = {};
    for (const x of M) {
      if (x.comp && !SYS.components.includes(x.comp)) out.issues.push(`零件「${x.comp}」唔喺系統卡（${x.id}「${x.text}」）`);
      if (!x.comp) out.issues.push(`${x.id}「${x.text}」manifest 冇寫 comp（屬邊款零件）`);
      if (x.comp === 'caption' || x.comp === 'hook') continue;
      tl.seek((x.start + x.end) / 2);
      const el = document.getElementById(x.id); if (!el) continue;
      const root = (hero && hero.contains(el)) ? hero : el;
      for (const n of [root, ...root.querySelectorAll('*')]) {
        if (exempt(n) || n.tagName === 'IMG') continue;
        const s = getComputedStyle(n);
        const ownText = [...n.childNodes].some(c => c.nodeType === 3 && c.textContent.trim()); const cs = [ownText ? s.color : 'transparent', s.backgroundColor];
        if (parseFloat(s.borderLeftWidth) > 0) cs.push(s.borderLeftColor);
        if (parseFloat(s.webkitTextStrokeWidth) > 0) cs.push(s.webkitTextStrokeColor);
        if (n instanceof SVGElement && n.tagName.toLowerCase() !== 'svg' && s.fill && s.fill !== 'none') cs.push(s.fill);
        for (const c of cs) { const h = hex(c); if (h) (colors[h] = colors[h] || { ids: new Set(), brandOnly: true }).ids.add(x.id), h && !['nametag'].includes(x.comp) && (colors[h].brandOnly = false); }
      }
    }
    out.colors = Object.fromEntries(Object.entries(colors).map(([k, v]) => [k, { ids: [...v.ids].slice(0, 4), brandOnly: v.brandOnly }]));
    return out;
  }, SYS);
  await b.close();
  const fails = [...R.issues], warns = [];
  const moving = R.tweens.filter(t => !['hold'].includes(t.kind));
  const easeSet = [...new Set(moving.map(t => t.ease))];
  easeSet.filter(e => !SYS.easing.includes(e)).forEach(e => fails.push(`緩動「${e}」唔喺系統卡：${moving.filter(t => t.ease === e).slice(0, 3).map(t => t.el + '@' + t.t).join('、')}`));
  const near = (d) => SYS.durations.some(a => Math.abs(a - d) <= 0.03);
  const badD = moving.filter(t => !near(t.d) && t.kind !== 'shake');
  [...new Set(badD.map(t => t.d))].forEach(d => fails.push(`時長 ${d}s 唔喺系統卡（${SYS.durations.join('/')}）：${badD.filter(t => t.d === d).slice(0, 3).map(t => t.el + '@' + t.t).join('、')}`));
  const entries = R.tweens.filter(t => !['exit', 'hold', 'shake', 'other'].includes(t.kind));
  const kinds = [...new Set(entries.map(t => t.kind))];
  kinds.filter(k => !SYS.entries.includes(k)).forEach(k => fails.push(`入場方式「${k}」唔喺系統卡：${entries.filter(t => t.kind === k).slice(0, 3).map(t => t.el + '@' + t.t).join('、')}`));
  R.tweens.filter(t => t.kind === 'other').slice(0, 5).forEach(t => warns.push(`分唔到類嘅 tween：${t.el}@${t.t}（${t.d}s ${t.ease}）`));
  // palette_fixed（品牌固定色：名牌、字幕、logo）只准喺品牌零件出現，其他零件用佢都算亂用
  const pal = new Set(Object.keys(SYS.palette).map(s => s.toLowerCase())), fixed = new Set(SYS.palette_fixed.map(s => s.toLowerCase()));
  Object.entries(R.colors).forEach(([h, v]) => {
    if (pal.has(h) || (fixed.has(h) && v.brandOnly)) return;
    fails.push(fixed.has(h) ? `品牌固定色 ${h} 用咗喺一般零件（${v.ids.join('、')}）` : `顏色 ${h} 唔喺系統卡色板（${v.ids.join('、')}）`);
  });
  const cnt = (arr) => Object.entries(arr.reduce((m, k) => (m[k] = (m[k] || 0) + 1, m), {})).map(([k, v]) => `${k}×${v}`).join('  ');
  console.log(`一致性（${SYS.name}）：${R.tweens.length} 個 tween`);
  console.log('  緩動：', cnt(moving.map(t => t.ease)));
  console.log('  入場：', cnt(entries.map(t => t.kind)));
  console.log('  時長：', cnt(moving.map(t => String(t.d))));
  console.log('  顏色：', Object.keys(R.colors).join(' '));
  warns.forEach(w => console.log(' !', w)); fails.forEach(f => console.log(' ✗', f));
  console.log(fails.length ? `✗ ${fails.length} 項唔跟系統卡，改完先渲染` : '✓ 一致性通過');
  process.exitCode = fails.length ? 1 : 0;
})();
