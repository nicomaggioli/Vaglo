#!/usr/bin/env python3
"""Local, no-cache static preview with byte ranges for video seeking."""
import os
import re
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

class NoCache(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Accept-Ranges', 'bytes')
        super().end_headers()

    def send_head(self):
        self.remaining = None
        path = self.translate_path(self.path)
        requested = self.headers.get('Range')
        if not requested or not os.path.isfile(path):
            return super().send_head()
        size = os.path.getsize(path)
        match = re.fullmatch(r'bytes=(\d*)-(\d*)', requested.strip())
        valid = bool(match and any(match.groups()) and size)
        if valid:
            first, last = match.groups()
            if first:
                start = int(first)
                end = min(int(last), size - 1) if last else size - 1
            else:
                start = max(0, size - int(last))
                end = size - 1
            valid = 0 <= start <= end < size
        if not valid:
            self.send_response(416)
            self.send_header('Content-Range', f'bytes */{size}')
            self.send_header('Content-Length', '0')
            self.end_headers()
            return None
        try:
            source = open(path, 'rb')
        except OSError:
            self.send_error(404, 'File not found')
            return None
        source.seek(start)
        self.remaining = end - start + 1
        self.send_response(206)
        self.send_header('Content-Type', self.guess_type(path))
        self.send_header('Content-Length', str(self.remaining))
        self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        self.end_headers()
        return source

    def copyfile(self, source, output):
        if self.remaining is None:
            return super().copyfile(source, output)
        while self.remaining:
            block = source.read(min(65536, self.remaining))
            if not block:
                break
            output.write(block)
            self.remaining -= len(block)

    def log_message(self, fmt, *args):
        pass

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8747
    print(f'Serving {os.getcwd()} on http://localhost:{port}', flush=True)
    ThreadingHTTPServer(('127.0.0.1', port), NoCache).serve_forever()
