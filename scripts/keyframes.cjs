// keyframes.cjs — 關鍵格靜圖（批核用，唔使 render 成條片）
// node scripts/keyframes.cjs <project_dir> <frames_dir(每秒 10 格 f_0001.jpg…)> <out_dir> [t1,t2,…]
// 冇俾時間 → 自動揀：每個非字幕畫面字出現後 0.6 秒（相隔 < 1.5 秒嘅合併）
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const [dir, framesDir, out, list] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(dir, 'index.html')); await p.waitForTimeout(1200);
  const M = await p.evaluate(() => JSON.parse(document.getElementById('fx-manifest').textContent));
  let T = list ? list.split(',').map(Number) : [];
  if (!T.length) for (const x of M.filter(x => x.kind !== 'caption').sort((a, b) => a.start - b.start)) {
    const t = +Math.min(x.start + 0.6, x.end - 0.05).toFixed(2); if (!T.length || t - T[T.length - 1] >= 1.5) T.push(t);
  }
  for (const t of T) {
    const f = path.resolve(framesDir, 'f_' + String(Math.round(t * 10) + 1).padStart(4, '0') + '.jpg');
    await p.evaluate(([t, f]) => {
      const v = document.getElementById('vid'); v.style.background = `url(${f}) center/cover`; v.removeAttribute('src');
      document.querySelectorAll('.clip').forEach(c => { if (c.id === 'fx051') return; const a = +c.dataset.start, d = +c.dataset.duration; c.style.visibility = (t >= a && t < a + d) ? 'visible' : 'hidden'; });
      window.__timelines.main.seek(t);
    }, [t, f]);
    await p.waitForTimeout(80);
    await p.screenshot({ path: path.join(out, `kf_${String(Math.round(t * 100)).padStart(5, '0')}.jpg`), type: 'jpeg', quality: 78 });
  }
  await b.close(); console.log(`✓ ${T.length} 張關鍵格 → ${out}`);
})();
