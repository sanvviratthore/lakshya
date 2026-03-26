#!/usr/bin/env python3
import http.server, socketserver, os

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*'); self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'); self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

if __name__ == '__main__':
    with socketserver.TCPServer(("", 3000), H) as httpd:
        print("[*] Lakshya Frontend Server running on http://localhost:3000"); print("[+] Serving from:", os.path.dirname(os.path.abspath(__file__))); httpd.serve_forever()
