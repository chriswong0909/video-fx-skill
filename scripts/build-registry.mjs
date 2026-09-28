#!/usr/bin/env node
// Scan effects/*/effect.md front matter -> registry.json (+ effects/INDEX.md)
import fs from 'node:fs'; import path from 'node:path'; import { fileURLToPath } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const dir = path.join(root, 'effects');
function parse(fm){ const o={}; for(const line of fm.split('\n')){ const m=line.match(/^([A-Za-z_]+):\s*(.*)$/); if(!m) continue;
  let v=m[2].replace(/\s+#.*$/,'').trim();
  if(v.startsWith('[')&&v.endsWith(']')) v=v.slice(1,-1).split(',').map(s=>s.trim().replace(/^["']|["']$/g,'')).filter(Boolean);
  else if(v==='true'||v==='false') v=(v==='true'); else v=v.replace(/^["']|["']$/g,''); o[m[1]]=v; } return o; }
const effects=[]; const errors=[];
for(const d of fs.readdirSync(dir).filter(n=>/^FX-\d{3}/.test(n)).sort()){
  const f=path.join(dir,d,'effect.md'); if(!fs.existsSync(f)){errors.push(`${d}: missing effect.md`);continue;}
  const txt=fs.readFileSync(f,'utf8'); const m=txt.match(/^---\n([\s\S]*?)\n---/); if(!m){errors.push(`${d}: no front matter`);continue;}
  const e=parse(m[1]); e.path=`effects/${d}`;
  e.has_snippet=fs.existsSync(path.join(dir,d,'snippet.html')); e.has_preview=fs.existsSync(path.join(dir,d,'preview.jpg'));
  const summ=txt.slice(m[0].length).match(/##\s*效果\s*\n+([^\n]+)/); e.summary=summ?summ[1].trim():'';
  for(const k of ['id','name','category']) if(!e[k]) errors.push(`${d}: missing ${k}`);
  effects.push(e);
}
const ids=new Set(effects.map(e=>e.id));
for(const e of effects) for(const k of ['pairs_with','conflicts_with']) for(const r of (e[k]||[])) if(!ids.has(r)) errors.push(`${e.id}: ${k} -> unknown ${r}`);
const byCat={}; for(const e of effects)(byCat[e.category]??=[]).push(e.id);
fs.writeFileSync(path.join(root,'registry.json'), JSON.stringify({generated:new Date().toISOString().slice(0,10),count:effects.length,by_category:byCat,effects},null,1)+'\n');
let md=`# 效果目錄（自動生成，勿手改）\n\n共 ${effects.length} 個效果\n\n| ID | 名稱 | 類別 | 情緒 | 適合 | 出處 |\n|---|---|---|---|---|---|\n`;
for(const e of effects) md+=`| [${e.id}](${e.path.replace('effects/','')}/effect.md) | ${e.name} | ${e.category} | ${(e.mood||[]).join(', ')} | ${(e.fits||[]).join(', ')} | ${e.source||''} |\n`;
fs.writeFileSync(path.join(dir,'INDEX.md'),md);
console.log(`registry.json: ${effects.length} effects`); if(errors.length){console.error('WARN:\n'+errors.join('\n')); process.exitCode=1;}
