"""
Simple webserver that returns 301 redirects to test Location header rewriting.
"""

import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, urlunparse


class RedirectHandler(BaseHTTPRequestHandler):
    """Handler that returns 301 redirects with relative Location headers."""
    
    def do_GET(self):
        """
        Handle GET requests:
        - Requests without trailing slash: 301 redirect to path with trailing slash
        - Requests with trailing slash: 200 OK
        - /redirect-to/target: 301 redirect to /target
        """
        # Parse the path to separate path and query string
        parsed = urlparse(self.path)
        path = parsed.path
        query = parsed.query
        
        if path.startswith("/redirect-to/"):
            # Extract the target path (remove /redirect-to prefix)
            target = path[len("/redirect-to"):]
            # Preserve query string if present
            if query:
                target = f"{target}?{query}"
            self.send_response(301)
            self.send_header("Location", target)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Redirecting...\n")
        elif not path.endswith("/"):
            # Add trailing slash, preserve query string
            new_path = path + "/"
            if query:
                new_location = f"{new_path}?{query}"
            else:
                new_location = new_path
            self.send_response(301)
            self.send_header("Location", new_location)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Redirecting...\n")
        else:
            # Normal response
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(f"Success: {self.path}\n".encode())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, required=True)
    args = ap.parse_args()
    
    httpd = HTTPServer(("127.0.0.1", args.port), RedirectHandler)
    httpd.serve_forever()
