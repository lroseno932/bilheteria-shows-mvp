#!/usr/bin/env python3
"""Serve public/ with the same security headers declared for Vercel."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEADERS = json.loads((ROOT / 'vercel.json').read_text())['headers'][0]['headers']

class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        for item in HEADERS:
            self.send_header(item['key'], item['value'])
        super().end_headers()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8794)
    args = parser.parse_args()
    server = ThreadingHTTPServer(('0.0.0.0', args.port), partial(Handler, directory=ROOT / 'public'))
    print(f'Preview ready on port {args.port}', flush=True)
    server.serve_forever()
