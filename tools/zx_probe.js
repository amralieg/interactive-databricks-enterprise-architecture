const fs = require('fs');
const vm = require('vm');
const html = fs.readFileSync(process.argv[2] || 'app/index.html', 'utf8');
const re = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;
let m, i = 0, errs = 0;
while ((m = re.exec(html))) {
  const attrs = m[1] || '';
  if (/\bsrc=/.test(attrs)) continue;
  if (/type=("|')?(application\/json|text\/)/i.test(attrs)) continue;
  const code = m[2];
  i++;
  try {
    new vm.Script(code, { filename: `inline-script-${i}` });
    console.log(`script #${i}: OK (${code.length} chars)`);
  } catch (e) {
    errs++;
    console.error(`script #${i}: SYNTAX ERROR -> ${e.message}`);
    const lineMatch = /inline-script-\d+:(\d+)/.exec(e.stack || '');
    if (lineMatch) {
      const ln = parseInt(lineMatch[1], 10);
      const lines = code.split('\n');
      for (let k = Math.max(0, ln - 3); k < Math.min(lines.length, ln + 2); k++) {
        console.error(`  ${k + 1}${k + 1 === ln ? ' >>' : '   '}| ${lines[k]}`);
      }
    }
  }
}
console.log(`\nchecked ${i} inline scripts, ${errs} error(s)`);
process.exit(errs ? 1 : 0);
