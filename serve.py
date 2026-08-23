#!/usr/bin/env python3
"""Local preview server that refuses to let the browser cache anything.

python -m http.server sends no Cache-Control at all, so browsers apply their own
heuristic and happily serve a stale index.html for hours. That is fine for a real
deploy and maddening while iterating.
"""
import sys
from http.server import SimpleHTTPRequestHandler, HTTPServer

class NoCache(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def log_message(self, fmt, *args):
        pass  # quiet

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8747
    print('serving %s on http://localhost:%d' % (__file__.rsplit('/', 1)[0] or '.', port))
    HTTPServer(('127.0.0.1', port), NoCache).serve_forever()
