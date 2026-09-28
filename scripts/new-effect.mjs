#!/usr/bin/env node
// usage: node scripts/new-effect.mjs "中文名" english-slug category
import fs from 'node:fs'; import path from 'node:path'; import { fileURLToPath } from 'node:url';
const [name,slug,category]=process.argv.slice(2);
if(!name||!slug||!category){console.error('usage: new-effect.mjs "中文名" english-slug category');process.exit(1);}
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..'); const dir=path.join(root,'effects');
const nums=fs.readdirSync(dir).map(n=>n.match(/^FX-(\d{3})/)).filter(Boolean).map(m=>+m[1]);
const id='FX-'+String((nums.length?Math.max(...nums):0)+1).padStart(3,'0');
const d=path.join(dir,`${id}-${slug}`); fs.mkdirSync(d,{recursive:true});
const today=new Date().toISOString().slice(0,10);
fs.writeFileSync(path.join(d,'effect.md'),`---
id: ${id}
name: ${name}
name_en: ${slug}
category: ${category}
tags: []
mood: []
fits: []
pairs_with: []
conflicts_with: []
needs: []
brand_color_ready: true
source: 
learned: ${today}
used_in: []
difficulty: medium
---

## 效果
（一句講清楚觀眾見到咩）

## 幾時用

## 幾時唔好用

## 參數同節奏

## 實作重點

## 已知限制
`);
fs.writeFileSync(path.join(d,'snippet.html'),`<!-- ${id} ${name}\n     依賴：\n     用法：貼入 composition，tl 由外部提供 -->\n`);
console.log(`created ${path.relative(root,d)}`);
