#!/usr/bin/env python3

import os
import socketserver

from http.server import SimpleHTTPRequestHandler as Handler

from lib.ensure_project_root import ensure_project_root


PORT = 8080

if __name__ == '__main__':
    ensure_project_root()
    os.chdir('www')
    with socketserver.TCPServer(("", PORT), Handler, True) as httpd:
        print(f'Serving {os.getcwd()} on Port: {PORT}')
        print(f'http://localhost:{PORT}')
        httpd.serve_forever()
