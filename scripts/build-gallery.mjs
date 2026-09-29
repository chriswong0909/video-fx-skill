#!/usr/bin/env node
// Build a self-contained visual catalogue of the effect library.
// Output: gallery/artifact.html (fragment for Claude Artifact publish) + gallery/index.html (open locally)
import fs from 'node:fs'; import path from 'node:path'; import { fileURLToPath } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const reg = JSON.parse(fs.readFileSync(path.join(root, 'registry.json'), 'utf8'));
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function md(src){ // tiny markdown -> html (headings, lists, code fences, inline code, paragraphs)
  const out=[]; let list=false, code=false, buf=[];
  const inline=t=>esc(t).replace(/`([^`]+)`/g,'<code>$1</code>');
  const closeList=()=>{ if(list){out.push('</ul>');list=false;} };
  for(const line of src.split('\n')){
    if(line.startsWith('```')){ if(code){out.push('<pre><code>'+esc(buf.join('\n'))+'</code></pre>');buf=[];code=false;} else {closeList();code=true;} continue; }
    if(code){buf.push(line);continue;}
    if(/^##\s+/.test(line)){closeList(); out.push('<h4>'+inline(line.replace(/^##\s+/,''))+'</h4>'); continue;}
    if(/^\s*-\s+/.test(line)){ if(!list){out.push('<ul>');list=true;} out.push('<li>'+inline(line.replace(/^\s*-\s+/,''))+'</li>'); continue;}
    if(!line.trim()){closeList(); continue;}
    closeList(); out.push('<p>'+inline(line)+'</p>');
  }
  closeList(); return out.join('\n');
}
const b64 = f => fs.existsSync(f) ? fs.readFileSync(f).toString('base64') : null;
const effects = reg.effects.map(e => {
  const dir = path.join(root, e.path);
  const txt = fs.readFileSync(path.join(dir, 'effect.md'), 'utf8').replace(/^---\n[\s\S]*?\n---\n?/, '');
  const vid = b64(path.join(dir, 'preview.mp4')); const img = b64(path.join(dir, 'preview.jpg'));
  const snip = fs.existsSync(path.join(dir, 'snippet.html')) ? fs.readFileSync(path.join(dir, 'snippet.html'), 'utf8') : '';
  return { id:e.id, name:e.name, en:e.name_en, cat:e.category, tags:e.tags||[], mood:e.mood||[], fits:e.fits||[], pairs:e.pairs_with||[], conf:e.conflicts_with||[],
    needs:e.needs||[], source:e.source||'', status:e.status||'active', vtypes:e.video_types||[], pace:e.pace||[], cjk_fit:e.cjk_fit||'', cjk_notes:e.cjk_notes||'', placement:e.placement||'', banned_reason:e.banned_reason||'', learned:e.learned||'', used:[].concat(e.used_in||[]), diff:e.difficulty||'', summary:e.summary||'',
    body: md(txt.replace(/##\s*效果\s*\n+[^\n]+\n?/, '')), snippet: snip,
    vid: vid ? 'data:video/mp4;base64,'+vid : null, img: img ? 'data:image/jpeg;base64,'+img : null };
});
const latest = effects.map(e=>e.learned).sort().pop() || '';
const data = JSON.stringify({ generated: reg.generated, latest, effects }).replace(/</g, '\\u003c');
const tpl = fs.readFileSync(path.join(root, 'gallery', 'template.html'), 'utf8');
const frag = tpl.replace('/*__DATA__*/null', data);
fs.writeFileSync(path.join(root, 'gallery', 'artifact.html'), frag);
fs.writeFileSync(path.join(root, 'gallery', 'index.html'), '<!doctype html><html lang="zh-Hant-HK"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>\n'+frag+'\n</body></html>');
console.log(`gallery: ${effects.length} effects, ${(Buffer.byteLength(frag)/1024/1024).toFixed(2)} MB`);
