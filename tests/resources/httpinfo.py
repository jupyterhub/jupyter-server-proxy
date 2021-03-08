from argparse import ArgumentParser
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
    p = ArgumentParser()
    p.add_argument('port', type=int)
    p.add_argument('--count', default=0, type=int, help='Exit after this number of requests, default is to never exit')
    args = p.parse_args()
    server_address = ('', args.port)
    httpd = HTTPServer(server_address, EchoRequestInfo)
    if args.count:
        for n in range(args.count):
            httpd.handle_request()
    else:
        httpd.serve_forever()
