#!/usr/bin/env node
'use strict';
/*
  One-shot migration: architectures/<id>.json -> architectures/<id>.yaml as the new
  canonical readable descriptor. Each file is verified (written YAML -> parse ->
  toTerse deep-equals the original JSON) BEFORE the JSON is removed, so a transform
  bug can never silently corrupt a board. manifest.json stays JSON (it is build
  metadata, not an architecture descriptor).
*/
const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');
const AS = require('../app/arch_schema.js');
const DUMP = { lineWidth: -1, noRefs: true, sortKeys: false };
const DIR = path.join(__dirname, '..', 'app', 'architectures');

function deepEq(a, b) { return JSON.stringify(sort(a)) === JSON.stringify(sort(b)); }
function sort(v) {
  if (Array.isArray(v)) return v.map(sort);
  if (v && typeof v === 'object') { const o = {}; for (const k of Object.keys(v).sort()) o[k] = sort(v[k]); return o; }
  return v;
}

const files = fs.readdirSync(DIR).filter(f => f.endsWith('.json') && f !== 'manifest.json');
let done = 0, fail = 0;
for (const f of files) {
  const jsonPath = path.join(DIR, f);
  const id = f.replace(/\.json$/, '');
  const orig = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
  const text = yaml.dump(AS.toReadable(orig), DUMP);
  const back = AS.toTerse(yaml.load(text));
  if (!deepEq(orig, back)) { fail++; console.error('REFUSE ' + f + ' : round-trip mismatch, JSON kept'); continue; }
  fs.writeFileSync(path.join(DIR, id + '.yaml'), text);
  fs.unlinkSync(jsonPath);
  done++;
}
console.log('converted ' + done + '/' + files.length + ' boards to YAML, ' + fail + ' refused');
process.exit(fail ? 1 : 0);
