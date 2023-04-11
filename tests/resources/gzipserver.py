import gzip
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO


class GzipServer(BaseHTTPRequestHandler):
    def do_GET(self):
        fileobj = BytesIO()
        f = gzip.GzipFile(fileobj=fileobj, mode="w")
        f.write(b"this is a test")
        f.close()
        content = fileobj.getvalue()
        self.send_response(200)
        self.send_header("Content-length", str(len(content)))
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Encoding", "gzip")
        self.end_headers()
        self.wfile.write(content)
        self.wfile.flush()


if __name__ == "__main__":
    port = int(sys.argv[1])
    server_address = ("", port)
    httpd = HTTPServer(server_address, GzipServer)
    httpd.serve_forever()
