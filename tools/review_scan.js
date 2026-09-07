// Per-board list of accelerator (use-case) tiles and connector (source) tiles,
// using the real ACCEL_BY_NAME + CONNECTORS + gates from index.html.
const fs = require('fs');
const html = fs.readFileSync(require('path').join(__dirname, '..', 'app', 'index.html'), 'utf8');
function extract(marker){
  const i = html.indexOf(marker); const b = html.indexOf('{', i);
  let d = 0, j = b, s = false, q = '';
  for(; j < html.length; j++){ const c = html[j], n = html[j+1];
    if(s){ if(c === '\\'){ j++; continue; } if(c === q) s = false; continue; }
    if(c === '/' && n === '/'){ while(j < html.length && html[j] !== '\n') j++; continue; }
    if(c === '/' && n === '*'){ j += 2; while(j < html.length && !(html[j] === '*' && html[j+1] === '/')) j++; j++; continue; }
    if(c === '"' || c === "'" || c === '`'){ s = true; q = c; continue; }
    if(c === '{') d++; else if(c === '}'){ d--; if(d === 0){ j++; break; } } }
  return html.slice(b, j);
}
const INDUSTRIES = Function('MEDALLION_ALSO','GX','return (' + extract('const INDUSTRIES = {') + ');')([], 'https://github.com/databricks-industry-solutions/');
const ACCEL_BY_NAME = Function('GX','return (' + extract('const ACCEL_BY_NAME = {') + ');')('https://github.com/databricks-industry-solutions/');
const CONNECTORS = Function('return (' + extract('const CONNECTORS = {') + ');')();
function accelFor(t){ return (t && (t.accel || (t.problem && ACCEL_BY_NAME[t.n]))) || null; }
function connectorFor(t){ if(!t || !t.cat || typeof t.n !== 'string') return null; for(const id in CONNECTORS){ if(CONNECTORS[id].re.test(t.n)) return CONNECTORS[id].n; } return null; }
function walk(node, acc, conn){
  if(Array.isArray(node)){ node.forEach(x => walk(x, acc, conn)); return; }
  if(!node || typeof node !== 'object') return;
  if(typeof node.n === 'string'){
    const a = accelFor(node); if(a) acc.push(node.n + '  ->  ' + a.n);
    const c = connectorFor(node); if(c) conn.push(node.n + '  ->  ' + c);
  }
  for(const k in node){ if(k === 'n') continue; walk(node[k], acc, conn); }
}
const keys = Object.keys(INDUSTRIES);
console.log('boards:', keys.length, '\n');
for(const key of keys){
  const acc = [], conn = [];
  walk(INDUSTRIES[key], acc, conn);
  const ua = [...new Set(acc)], uc = [...new Set(conn)];
  if(!ua.length && !uc.length) continue;
  console.log('=== ' + key + '  (accel:' + ua.length + '  conn:' + uc.length + ') ===');
  if(ua.length){ console.log('  ACCEL:'); ua.forEach(x => console.log('    ' + x)); }
  if(uc.length){ console.log('  CONN:'); uc.forEach(x => console.log('    ' + x)); }
  console.log('');
}
