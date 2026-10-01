// fx-shot.cjs — 效果 snippet 截圖（token 化前後對比、唔同預設對比）
// node scripts/fx-shot.cjs <effects_dir> <out_dir> [tokens.css|-] [t=1.6 | auto | times.json] [bg.jpg]
// auto：每個效果截 6 個時間點（之後用 fx-pick.py 揀畫面最多嘢嗰格，寫 times.json）
// 每個效果砌一頁：1080×1920 + 講者底圖 + (tokens) + snippet，seek 到 t 截圖（270×480）。
// 輸出 <out>/FX-###.jpg 同 <out>/report.json（錯誤、畫面字數）
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const [fxDir, out, tokPath, tArg, bgArg] = process.argv.slice(2);
const TIMES = tArg === 'auto' ? [0.5, 1.0, 1.6, 2.2, 2.8, 3.4] : null; const TMAP = tArg && /\.json$/.test(tArg) ? JSON.parse(fs.readFileSync(tArg, 'utf8')) : null; const T_SEEK = +(TIMES || TMAP ? 1.6 : (tArg || 1.6)); fs.mkdirSync(out, { recursive: true });
const ROOT = path.resolve(__dirname, '..');
const gsapSrc = fs.readFileSync(fs.existsSync(path.join(ROOT, 'scripts/vendor/gsap.min.js')) ? path.join(ROOT, 'scripts/vendor/gsap.min.js') : process.env.GSAP_JS);
const tokens = tokPath && tokPath !== '-' ? fs.readFileSync(tokPath, 'utf8') : '';
const SAMPLE = fs.readFileSync(process.env.FX_SAMPLE || path.join(ROOT, 'scripts/vendor/sample.jpg'));
const bg = bgArg ? 'data:image/jpeg;base64,' + fs.readFileSync(bgArg).toString('base64') : '';
const PRE = `
window.tl = gsap.timeline({paused:true}); tl.to({}, {duration:4}, 0);
const PLURAL = /s$|items|rows|words|list|cards|labels|points|steps/i;
window.T = new Proxy({}, {get:(o,k)=> typeof k!=='string' ? undefined : PLURAL.test(k) ? [0.4,0.8,1.2,1.6,2.0] : ({start:0.2,end:2.8,dur:2.6,duration:2.6,label:0.6,in:0.2,out:2.6}[k] ?? 0.6)});
window.PHRASES=[["示範字幕效果",0.1,3.5]]; window.WORDS=[["示範",0.2,0.8],["效果",0.8,1.4],["字幕",1.4,3]];
window.ITEMS=window.T.items; window.SHOTS=[[0,1.2,'W','cut'],[1.2,2.4,'M','smooth'],[2.4,4,'C','smooth']]; window.CH=[{t:0},{t:1.5},{t:3}]; window.W1=0.4; window.W2=1.4; window.W3=2.4; window.Q=[0.4,1.2,2.0]; window.START=0.2; window.END=2.8;`;
(async () => {
  const b = await chromium.launch(); const report = {};
  const dirs = fs.readdirSync(fxDir).filter(d => /^FX-\d+/.test(d) && fs.existsSync(path.join(fxDir, d, 'snippet.html'))).sort();
  for (const d of dirs) {
    const id = d.slice(0, 6); const snip = fs.readFileSync(path.join(fxDir, d, 'snippet.html'), 'utf8');
    const html = `<!doctype html><html><head><meta charset="utf-8"><base href="http://fx.local/"><style>
@font-face{font-family:SansTC;src:local("Noto Sans CJK HK Black"),local("Noto Sans CJK TC Black");font-weight:100 900}
@font-face{font-family:SerifTC;src:local("Noto Serif CJK TC Bold"),local("Noto Serif CJK TC");font-weight:100 900}
@font-face{font-family:Round;src:local("Noto Sans CJK HK Black");font-weight:100 900}
html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#000}
#main{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:SansTC}
#cam{position:absolute;inset:0;z-index:0;overflow:hidden}#camInner{position:absolute;inset:0;transform-origin:540px 420px}
#vid{position:absolute;inset:0;background:#556 url(${bg}) center/cover}
.clip{visibility:visible!important}
</style>${tokens ? '<style>' + tokens + '</style>' : ''}<script>${gsapSrc}</script><script>${PRE}</script></head>
<body><div id="main" data-composition-id="main"><div id="cam"><div id="camInner"><div id="vid"></div></div></div>
${snip}
</div></body></html>`;
    const p = await b.newPage({ viewport: { width: 1080, height: 1920 } }); const errs = [];
    p.on('pageerror', e => errs.push(String(e.message).slice(0, 120)));
    // 效果要用嘅素材（assets/…）冇喺庫入面：一律用示範相頂上，等截圖睇到版面
    await p.route('http://fx.local/**', r => { const u = r.request().url();
      if (/\.svg$/.test(u)) return r.fulfill({ contentType: 'image/svg+xml', body: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><rect width="10" height="10" fill="#ddd"/></svg>' });
      return r.fulfill({ contentType: 'image/jpeg', body: SAMPLE }); });
    await p.setContent(html, { waitUntil: 'load' }); await p.waitForTimeout(150);
    const seekShot = async (t, file) => {
      const info = await p.evaluate((t) => { try { (window.__timelines?.main || window.tl).seek(t); } catch (e) { return { seekErr: String(e) }; }
        return { text: (document.getElementById('main').innerText || '').replace(/\s+/g, '').length }; }, t);
      await p.waitForTimeout(60); fs.writeFileSync(file, await p.screenshot({ type: 'png' })); return info; };
    let info;
    if (TIMES) { for (const t of TIMES) info = await seekShot(t, path.join(out, `${id}@${t}.png`)); }
    else info = await seekShot(TMAP && TMAP[id] !== undefined ? TMAP[id] : T_SEEK, path.join(out, id + '.png'));
    report[id] = { errs, ...info }; await p.close();
  }
  await b.close(); fs.writeFileSync(path.join(out, 'report.json'), JSON.stringify(report, null, 1));
  const bad = Object.entries(report).filter(([k, v]) => v.errs.length || v.seekErr);
  console.log(`✓ ${dirs.length} 個效果截圖 → ${out}｜有錯 ${bad.length} 個：${bad.map(([k]) => k).join(' ')}`);
})();
