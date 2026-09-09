'use strict';
/*
  Shared, comment/string-aware literal extractor for app/index.html.

  Both tools/split_modules.js (data externalisation) and tools/build_i18n.js
  (translation corpus) need to read the ARCH / INDUSTRIES / LINKS / REFERENCES /
  ACCEL_BY_NAME / CONNECTORS / INDUSTRY_CATALOG literals straight out of the HTML.
  Keeping one extractor here is the single source of truth; a second copy would
  drift the brace/bracket matching the two tools depend on.
*/

// The only in-file consts the data literals reference. Injected so a literal
// evaluates in isolation regardless of which one it happens to mention:
//   ACCEL_BY_NAME builds repo URLs from GX; CONNECTORS slugs off LFC; the
//   medallion overlay references MEDALLION_ALSO. Everything else is self-data.
const SANDBOX = {
  GX: 'https://github.com/databricks-industry-solutions/',
  LFC: 'ingestion/lakeflow-connect/',
  MEDALLION_ALSO: [],
};

// Return [start, end) offsets of the balanced literal opened by `open` at/after
// `marker`, skipping // and /* */ comments and string bodies so a brace inside a
// comment or a quoted string never miscounts depth.
function literalBounds(src, marker, open, close) {
  const mi = src.indexOf(marker);
  if (mi < 0) throw new Error('marker not found: ' + marker);
  const start = src.indexOf(open, mi);
  if (start < 0) throw new Error('open "' + open + '" not found after: ' + marker);
  let depth = 0, j = start, inStr = false, q = '';
  for (; j < src.length; j++) {
    const c = src[j], n = src[j + 1];
    if (inStr) { if (c === '\\') { j++; continue; } if (c === q) inStr = false; continue; }
    if (c === '/' && n === '/') { while (j < src.length && src[j] !== '\n') j++; continue; }
    if (c === '/' && n === '*') { j += 2; while (j < src.length && !(src[j] === '*' && src[j + 1] === '/')) j++; j++; continue; }
    if (c === '"' || c === "'" || c === '`') { inStr = true; q = c; continue; }
    if (c === open) depth++;
    else if (c === close) { depth--; if (depth === 0) { j++; break; } }
  }
  if (depth !== 0) throw new Error('unbalanced literal for: ' + marker);
  return [start, j];
}

function extractObjectText(src, marker) {
  const [a, b] = literalBounds(src, marker, '{', '}');
  return { text: src.slice(a, b), start: a, end: b };
}
function extractArrayText(src, marker) {
  const [a, b] = literalBounds(src, marker, '[', ']');
  return { text: src.slice(a, b), start: a, end: b };
}

function evalText(text) {
  const keys = Object.keys(SANDBOX);
  const vals = keys.map(k => SANDBOX[k]);
  // eslint-disable-next-line no-new-func
  return Function(...keys, 'return (' + text + ');')(...vals);
}

function evalObject(src, marker) { return evalText(extractObjectText(src, marker).text); }
function evalArray(src, marker) { return evalText(extractArrayText(src, marker).text); }

module.exports = {
  SANDBOX,
  literalBounds,
  extractObjectText,
  extractArrayText,
  evalText,
  evalObject,
  evalArray,
};
