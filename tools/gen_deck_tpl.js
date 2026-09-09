#!/usr/bin/env node
'use strict';
/*
  Generate DECK_TPL language blocks for the new languages. The five section
  blurbs, count captions, model-link, close-title and cloud-line carry {ind}/{n}/
  {plat}/{cloud} placeholders, so they are authored as per-language templates in
  app/index.html rather than value-keyed through T(). The original six languages
  (en/fr/es/zh/ar/hi) were hand-authored; the ten new ones fell back to English,
  which is why an exported Japanese/German deck rendered the blurbs in English.

  This machine-translates DECK_TPL.en into the new languages, reusing build_i18n's
  exact clients5 endpoint + glossary masking + echo/empty individual retry, and
  masks the {..} placeholders with an ASCII sentinel that survives every target
  script so the runtime dt() can still fill them. Output is a JS block per
  language, printed for insertion into the DECK_TPL object. index.html stays the
  single source of DECK_TPL.en (extracted via lib_extract).
*/
const fs = require('fs');
const path = require('path');
const { evalObject } = require('./lib_extract');
const { translateOne, looksTranslatable } = require('./build_i18n');

const HTML = path.join(__dirname, '..', 'app', 'index.html');
const NEW = ['de', 'pt', 'nl', 'ja', 'it', 'sv', 'ko', 'da', 'fi', 'he'];

// Two things must reach dt() verbatim that translateOne's glossary does NOT cover:
//   1. the {ind}/{n}/{plat}/{cloud} placeholders, and
//   2. compound brands the hand-authored six languages keep intact ("Databricks
//      Apps", "Metric Views", ...) but that the runtime glossary only has as the
//      bare token "Databricks" (so "Apps" would translate to "Aplicativos").
// Both are wrapped in an ASCII sentinel (Zx<i>xZ, distinct from translateOne's
// own Zq<i>qZ so the two masking layers never collide) that survives every target
// script unchanged, then restored after translation.
const KEEP = [
  'Databricks Data Intelligence Platform', 'Databricks Apps', 'Metric Views',
  'Databricks', 'Lakebase', 'Lakehouse', 'lakehouse', 'AI/BI'
].sort((a, b) => b.length - a.length);
const KEEP_RE = new RegExp(KEEP.map(s => s.replace(/[.*+?^${}()|[\]\\/]/g, '\\$&')).join('|') + '|\\{\\w+\\}', 'g');

function mask(s){ const f = []; const m = s.replace(KEEP_RE, x => { const i = f.length; f.push(x); return 'Zx' + i + 'xZ'; }); return { m, f }; }
function unmask(s, f){ return String(s).replace(/Zx(\d+)xZ/g, (_, i) => f[+i] != null ? f[+i] : ''); }

// Translate one template, guaranteeing a NON-EMPTY result (an empty string would
// make dt() render blank). The clients5 endpoint occasionally returns "" or the
// masked source; retry a few times. An echo is only a real miss for genuine prose
// (the five blurbs); short count captions like "{n} agent" legitimately equal the
// source in cognate languages (Swedish "agent"), so those accept the echo. If
// every attempt is empty we keep the best non-empty seen, else throw.
async function tr(s, tl){
  if(!s) return s;
  const { m, f } = mask(s);
  const prose = looksTranslatable(m);
  let best = '';
  for(let attempt = 0; attempt < 4; attempt++){
    const raw = await translateOne(m, tl);
    if(typeof raw !== 'string' || !raw.trim()) continue;   // empty => retry
    best = raw;
    if(!prose || raw.trim() !== m.trim()) return unmask(raw, f);   // good (or short-caption echo ok)
  }
  if(best.trim()) return unmask(best, f);
  throw new Error('translation returned empty after retries: [' + tl + '] ' + s);
}

// ASCII-only JS string literal, matching the existing \uXXXX style in DECK_TPL.
function jsStr(s){
  let r = '';
  for(const ch of s){
    const c = ch.codePointAt(0);
    if(ch === '"') r += '\\"';
    else if(ch === '\\') r += '\\\\';
    else if(c < 0x20) r += '\\u' + c.toString(16).padStart(4, '0');
    else if(c > 0x7e){
      if(c > 0xffff){
        const h = Math.floor((c - 0x10000) / 0x400) + 0xd800;
        const l = (c - 0x10000) % 0x400 + 0xdc00;
        r += '\\u' + h.toString(16).padStart(4, '0') + '\\u' + l.toString(16).padStart(4, '0');
      } else r += '\\u' + c.toString(16).padStart(4, '0');
    } else r += ch;
  }
  return '"' + r + '"';
}

(async function main(){
  const EN = evalObject(fs.readFileSync(HTML, 'utf8'), 'const DECK_TPL =').en;
  const keys = Object.keys(EN);
  const blocks = [];
  for(const lang of NEW){
    const obj = {};
    for(const k of keys){ obj[k] = await tr(EN[k], lang); process.stderr.write('.'); }
    const body = keys.map(k => '    ' + k + ':' + jsStr(obj[k])).join(',\n');
    blocks.push('  ' + lang + ': {\n' + body + '\n  }');
    process.stderr.write(' ' + lang + '\n');
  }
  fs.writeFileSync('/tmp/deck_tpl_blocks.txt', blocks.join(',\n') + '\n');
  process.stderr.write('WROTE /tmp/deck_tpl_blocks.txt (' + NEW.length + ' langs x ' + keys.length + ' keys)\n');
})();
