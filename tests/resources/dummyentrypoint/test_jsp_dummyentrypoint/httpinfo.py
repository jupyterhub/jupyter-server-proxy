"""
Simple webserver to respond with an echo of the sent request.
"""

import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer


class EchoRequestInfo(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(f"{self.requestline}\n".encode())
        self.wfile.write(f"{self.headers}\n".encode())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int)
    args = ap.parse_args()

    httpd = HTTPServer(("127.0.0.1", args.port), EchoRequestInfo)
    httpd.serve_forever()
