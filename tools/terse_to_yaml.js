#!/usr/bin/env node
'use strict';
/*
  Bridge between the Python authoring tool (inject_industries.py) and the single
  JS schema transform (app/arch_schema.js), so the readable YAML descriptor format
  is never re-implemented in Python and the two cannot drift. Two modes:
    (default)        stdin  = terse board JSON   -> stdout = readable YAML descriptor
    --terse <file>   reads a YAML descriptor      -> stdout = terse board JSON
*/
const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');
const AS = require(path.join(__dirname, '..', 'app', 'arch_schema.js'));
const DUMP = { lineWidth: -1, noRefs: true, sortKeys: false };

const ti = process.argv.indexOf('--terse');
if (ti >= 0) {
  const terse = AS.toTerse(yaml.load(fs.readFileSync(process.argv[ti + 1], 'utf8')));
  process.stdout.write(JSON.stringify(terse));
} else {
  const terse = JSON.parse(fs.readFileSync(0, 'utf8'));   // stdin
  process.stdout.write(yaml.dump(AS.toReadable(terse), DUMP));
}
