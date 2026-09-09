// Count Business + Technical team tiles per board's People pocket, to size the
// blast radius of changing PPL_BUSINESS_CAP.
const fs = require('fs');
const path = require('path');
const html = fs.readFileSync(path.join(__dirname, '..', 'app', 'index.html'), 'utf8');
function extract(marker){
  const i = html.indexOf(marker);
  if(i < 0) throw new Error('not found: ' + marker);
  let depth = 0, started = false, out = '';
  for(let j = i + marker.length - 1; j < html.length; j++){
    const c = html[j];
    if(c === '{'){ depth++; started = true; }
    if(started) out += c;
    if(c === '}'){ depth--; if(depth === 0) break; }
  }
  return out;
}
const INDUSTRIES = Function('MEDALLION_ALSO','GX','return (' + extract('const INDUSTRIES = {') + ');')([], 'https://github.com/databricks-industry-solutions/');
const rows = [];
for(const key of Object.keys(INDUSTRIES)){
  const ppl = ((INDUSTRIES[key].rails || {}).ppl) || [];
  let biz = 0, tech = 0, other = 0;
  ppl.forEach(g => {
    const n = (g.tiles || []).length;
    if(/^business$/i.test(g.box || '')) biz = n;
    else if(/^technical$/i.test(g.box || '')) tech = n;
    else other += n;
  });
  rows.push({ key, biz, tech, other, total: biz + tech + other });
}
rows.sort((a,b)=> b.biz - a.biz || b.total - a.total);
console.log('boards:', rows.length);
console.log('\nBoards with Business > 5 (currently capped, hiding tiles):');
rows.filter(r=>r.biz > 5).forEach(r=> console.log('  ' + r.key + '  biz=' + r.biz + ' tech=' + r.tech + ' other=' + r.other));
console.log('\nBoards with Business == 6:');
rows.filter(r=>r.biz === 6).forEach(r=> console.log('  ' + r.key));
console.log('\nTop 12 by business count:');
rows.slice(0,12).forEach(r=> console.log('  ' + r.key + '  biz=' + r.biz + ' tech=' + r.tech + ' other=' + r.other + ' total=' + r.total));
console.log('\nMax business:', rows[0].biz, '(' + rows[0].key + ')');
console.log('Max total pocket tiles:', Math.max(...rows.map(r=>r.total)), '(' + rows.reduce((a,b)=>b.total>a.total?b:a).key + ')');
