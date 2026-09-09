// Exhaustive review: walk EVERY tile in every board (all rails, bands, top, cloud)
// applying the real connectorFor gate (t.cat) + CONNECTORS regexes from index.html,
// and report matches grouped by where they sit so any non-source match is visible.
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
const INDUSTRIES = Function('MEDALLION_ALSO','GX','return (' + extract('const INDUSTRIES = {') + ');')([], 'x');
const CONNECTORS = Function('return (' + extract('const CONNECTORS = {') + ');')();
function connectorFor(t){
  if(!t || !t.cat || typeof t.n !== 'string') return null;
  for(const id in CONNECTORS){ if(CONNECTORS[id].re.test(t.n)) return id; }
  return null;
}
// Walk a board, tracking which rail/section a tile with .cat sits in.
const byRail = {}; let total = 0;
function walk(node, loc){
  if(Array.isArray(node)){ node.forEach(x => walk(x, loc)); return; }
  if(!node || typeof node !== 'object') return;
  if(typeof node.n === 'string' && typeof node.cat === 'string'){
    const id = connectorFor(node);
    if(id){ total++; (byRail[loc] = byRail[loc] || []).push(node.n + ' -> ' + id); }
  }
  for(const k in node){ if(k === 'n' || k === 'cat') continue;
    const nl = (k === 'src' || k === 'ing' || k === 'ppl' || k === 'cons' || k === 'top' || k === 'cloud' || k === 'bands') ? k : loc;
    walk(node[k], nl);
  }
}
for(const key in INDUSTRIES) walk(INDUSTRIES[key], 'root');
console.log('Total connector-marked tiles across all boards/rails:', total);
console.log('\n=== grouped by rail/section (anything outside src/ing is worth a look) ===');
Object.keys(byRail).sort().forEach(loc => {
  const uniq = [...new Set(byRail[loc])];
  console.log('\n['+loc+'] '+byRail[loc].length+' hits, '+uniq.length+' distinct');
  uniq.forEach(x => console.log('   '+x));
});
