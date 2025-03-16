#!/usr/bin/env python3

import sys
import os
import socketserver

from http.server import SimpleHTTPRequestHandler as Handler

WWW = os.path.join(os.path.dirname(sys.argv[0]), 'www')

PORT = 8080

if __name__ == '__main__':
    os.chdir(WWW)
    with socketserver.TCPServer(("", PORT), Handler, True) as httpd:
        print(f'Serving {WWW} on Port: {PORT}')
        print(f'http://localhost:{PORT}')
        httpd.serve_forever()
