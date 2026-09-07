#!/usr/bin/env node
'use strict';
/*
  Ship-blocking gate: the terse<->readable descriptor transform is LOSSLESS.
  For every board, assert toTerse(toReadable(d)) deep-equals d. A single mismatch
  means the YAML round-trip would silently drop or corrupt board content, so this
  exits non-zero and prints the first differing path.
*/
const fs = require('fs');
const path = require('path');
const AS = require('../app/arch_schema.js');
const yaml = require('js-yaml');

const DIR = path.join(__dirname, '..', 'app', 'architectures');
// Dump options must match the runtime/download path so the gate proves the exact
// text round-trip authors will hit. lineWidth:-1 keeps prose on one line.
const DUMP = { lineWidth: -1, noRefs: true, sortKeys: false };

// Order-independent deep diff; returns first differing path or null.
function diff(a, b, p) {
  p = p || '';
  if (a === b) return null;
  const ta = a === null ? 'null' : Array.isArray(a) ? 'array' : typeof a;
  const tb = b === null ? 'null' : Array.isArray(b) ? 'array' : typeof b;
  if (ta !== tb) return p + ' : type ' + ta + ' != ' + tb;
  if (ta === 'array') {
    if (a.length !== b.length) return p + ' : len ' + a.length + ' != ' + b.length;
    for (let i = 0; i < a.length; i++) { const d = diff(a[i], b[i], p + '[' + i + ']'); if (d) return d; }
    return null;
  }
  if (ta === 'object') {
    const ka = Object.keys(a).sort(), kb = Object.keys(b).sort();
    if (ka.join(',') !== kb.join(',')) return p + ' : keys {' + ka.join(',') + '} != {' + kb.join(',') + '}';
    for (const k of ka) { const d = diff(a[k], b[k], p + '.' + k); if (d) return d; }
    return null;
  }
  return p + ' : ' + JSON.stringify(a) + ' != ' + JSON.stringify(b);
}

const files = fs.readdirSync(DIR).filter(f => f.endsWith('.yaml'));
let ok = 0, fail = 0;
for (const f of files) {
  // Canonical is now YAML. Prove the round-trip is idempotent: the terse form the
  // renderer/build consume must survive a re-download (terse -> readable -> YAML
  // text -> parse -> terse) unchanged. A drift here means download/edit/upload
  // would mutate a board the author never touched.
  const d = AS.toTerse(yaml.load(fs.readFileSync(path.join(DIR, f), 'utf8')));
  const back = AS.toTerse(yaml.load(yaml.dump(AS.toReadable(d), DUMP)));
  const dd = diff(d, back, f);
  if (dd) { fail++; console.error('FAIL ' + dd); }
  else ok++;
}
console.log('arch_schema YAML round-trip: ' + ok + '/' + files.length + ' idempotent, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
