"""
Simple webserver to respond with an echo of the sent request. It can listen to
either a tcp port or a unix socket.
"""
import argparse
import socket
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path


class EchoRequestInfo(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(f"{self.requestline}\n".encode())
        self.wfile.write(f"{self.headers}\n".encode())

    def address_string(self):
        """
        Overridden to fix logging when serving on Unix socket.

        FIXME: There are still broken pipe messages showing up in the jupyter
               server logs when running tests with the unix sockets.
        """
        if isinstance(self.client_address, str):
            return self.client_address  # Unix sock
        return super().address_string()


if sys.platform != "win32":

    class HTTPUnixServer(HTTPServer):
        address_family = socket.AF_UNIX


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int)
    ap.add_argument("--unix-socket")
    args = ap.parse_args()

    if args.unix_socket:
        unix_socket = Path(args.unix_socket)
        if unix_socket.exists():
            unix_socket.unlink()
        httpd = HTTPUnixServer(args.unix_socket, EchoRequestInfo)
    else:
        httpd = HTTPServer(("127.0.0.1", args.port), EchoRequestInfo)
    httpd.serve_forever()
