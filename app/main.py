"""Static server for IDEA on Databricks Apps.

The diagram is one self-contained HTML file with no build step and no backend,
so the whole server is the standard library. Adding FastAPI or Flask here would
mean a requirements.txt, a pip resolve on every deploy, and a dependency set to
keep patched, all to hand back a file that never changes at runtime.

Databricks Apps terminates TLS, applies workspace authentication and routes the
request in, so this process only has to answer on the port it is given.
"""

import os
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
# Apps injects the port. 8000 is the platform default and is only the fallback
# for running this file straight from a laptop.
PORT = int(os.environ.get("DATABRICKS_APP_PORT", "8000"))


class Handler(SimpleHTTPRequestHandler):
    # 1.0 closes the socket after every response, which costs a fresh connection
    # for each of the page's sub-requests through the Apps proxy.
    protocol_version = "HTTP/1.1"

    def end_headers(self):
        # The page keeps its state in localStorage, so a stale cached copy after
        # an upgrade shows an old diagram against new saved state.
        self.send_header("Cache-Control", "no-store, max-age=0")
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()

    def log_message(self, fmt, *args):
        # Apps collects stdout as the app log; the default handler writes to
        # stderr, which surfaces every page view as an error line.
        sys.stdout.write("%s %s\n" % (self.address_string(), fmt % args))
        sys.stdout.flush()

    def list_directory(self, path):
        # There is nothing to browse here, and an auto-generated listing would
        # publish app.yaml and this file to anyone who trims a URL.
        self.send_error(404)
        return None

    def send_error(self, code, message=None, explain=None):
        # Anything that is not a real file is the diagram: there is exactly one
        # page, and a mistyped path should land on it rather than on a 404. The
        # flag stops a missing index.html from bouncing between the two forever.
        if code == 404 and not getattr(self, "_fellback", False):
            self._fellback = True
            self.path = "/index.html"
            return SimpleHTTPRequestHandler.do_GET(self)
        return super().send_error(code, message, explain)


def main():
    handler = partial(Handler, directory=HERE)
    server = ThreadingHTTPServer(("0.0.0.0", PORT), handler)
    print("IDEA serving %s on port %d" % (HERE, PORT), flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
