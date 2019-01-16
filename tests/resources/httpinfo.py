from http.server import HTTPServer, BaseHTTPRequestHandler
import sys

class EchoRequestInfo(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write('{}\n'.format(self.requestline).encode())
        self.wfile.write('{}\n'.format(self.headers).encode())


if __name__ == '__main__':
    port = int(sys.argv[1])
    server_address = ('', port)
    httpd = HTTPServer(server_address, EchoRequestInfo)
    httpd.serve_forever()
