'use strict';
/*
  Shared static server for the Playwright gates. Serves app/ with the production
  server's semantics (app/main.py): a known file is returned with its MIME type;
  any unknown path returns index.html as HTML/200 (the single-page fallback), so
  the loadIndustry content-type guard is exercised for a bad industry id.

  Since the data-modularisation split, industries and resources are fetched from
  architectures/*.json and resources/*.json. `fetch()` does not work on file://,
  so every gate that drives industry loading MUST serve over HTTP through this
  helper instead of opening index.html directly. Kept in one place so the four
  gates and the smoke tests share identical serving behaviour.
*/
const http = require('http');
const fs = require('fs');
const path = require('path');

const APP_ROOT = path.join(__dirname, '..', 'app');
const MIME = { '.html': 'text/html', '.json': 'application/json', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.yaml': 'text/yaml', '.yml': 'text/yaml' };

// Start a server on an ephemeral port. Resolves to the http.Server; read its
// port via server.address().port. Close it with server.close() when done.
function serve(root) {
  const base = root || APP_ROOT;
  return new Promise(res => {
    const s = http.createServer((req, r) => {
      let p = decodeURIComponent(req.url.split('?')[0]);
      if (p === '/') p = '/index.html';
      const fp = path.join(base, p);
      fs.readFile(fp, (e, d) => {
        if (e) { // production fallback: any unknown path is the single page
          r.writeHead(200, { 'Content-Type': 'text/html' });
          r.end(fs.readFileSync(path.join(base, 'index.html')));
          return;
        }
        r.writeHead(200, { 'Content-Type': MIME[path.extname(fp)] || 'application/octet-stream' });
        r.end(d);
      });
    });
    s.listen(0, () => res(s));
  });
}

module.exports = { serve, APP_ROOT, MIME };
