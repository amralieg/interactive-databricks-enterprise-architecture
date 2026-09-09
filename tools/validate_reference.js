#!/usr/bin/env node
'use strict';
const fs = require('fs');
const path = require('path');

const APP = path.join(__dirname, '..', 'app', 'index.html');
const html = fs.readFileSync(APP, 'utf8');

function extractLiteral(src, marker){
  const i = src.indexOf(marker);
  if(i < 0) throw new Error('marker not found: ' + marker);
  const braceStart = src.indexOf('{', i);
  let depth = 0, j = braceStart, inStr = false, q = '';
  for(; j < src.length; j++){
    const c = src[j], n = src[j+1];
    if(inStr){ if(c === '\\'){ j++; continue; } if(c === q) inStr = false; continue; }
    if(c === '/' && n === '/'){ while(j < src.length && src[j] !== '\n') j++; continue; }
    if(c === '/' && n === '*'){ j += 2; while(j < src.length && !(src[j] === '*' && src[j+1] === '/')) j++; j++; continue; }
    if(c === '"' || c === "'" || c === '`'){ inStr = true; q = c; continue; }
    if(c === '{') depth++;
    else if(c === '}'){ depth--; if(depth === 0){ j++; break; } }
  }
  return src.slice(braceStart, j);
}

const ARCH = eval('(' + extractLiteral(html, 'const ARCH = {') + ')');

const DATA_SHAPES = new Set(['structured', 'semi-structured', 'unstructured']);
const errs = [];

function checkFlow(where, flow){
  if(!flow || typeof flow !== 'object'){ errs.push(`${where}: lane must be an object`); return; }
  if(!Array.isArray(flow.types) || !flow.types.length) errs.push(`${where}: lane missing non-empty types`);
  else { const bad = flow.types.filter(t => !DATA_SHAPES.has(t)); if(bad.length) errs.push(`${where}: bad data shape(s) ${bad.join(', ')}`); }
  if(!flow.vol) errs.push(`${where}: lane missing vol`);
  if(!flow.interval) errs.push(`${where}: lane missing interval`);
}

function checkSourceTile(where, t, needCat){
  const n = t.n;
  if(needCat && !t.cat) errs.push(`${where} :: ${n}: missing cat`);
  if(!t.what) errs.push(`${where} :: ${n}: missing what`);
  if(!t.users) errs.push(`${where} :: ${n}: missing users`);
  const d = t.dataOut;
  if(!d || typeof d !== 'object' || !(d.batch || d.stream)){ errs.push(`${where} :: ${n}: missing dataOut (batch/stream)`); return; }
  if(d.batch) checkFlow(`${where} :: ${n} batch`, d.batch);
  if(d.stream) checkFlow(`${where} :: ${n} stream`, d.stream);
}

for(const g of (ARCH.rails.src.groups || []))
  for(const t of (g.tiles || [])) checkSourceTile(`reference src / ${g.box}`, t, false);

for(const g of (ARCH.rails.ing.groups || [])){
  if(g.box === 'Cloud ETL') continue;
  for(const t of (g.tiles || [])) checkSourceTile(`reference ing / ${g.box}`, t, false);
}

for(const cloud of ['aws', 'azure', 'gcp']){
  const p = ARCH.cloud.providers[cloud];
  for(const t of (p.fed || [])) checkSourceTile(`federation / ${cloud}`, t, true);
}

for(const e of errs) console.log('  ERR', e);
console.log(`reference + federation enrichment errors: ${errs.length}`);
if(errs.length){ process.exit(1); }
console.log('PASS');
