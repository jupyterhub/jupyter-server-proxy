#vim: set et ts=4 sw=4:
import logging
import tornado.httpclient

from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler

logger = logging.getLogger('nbserverproxy')

# From https://github.com/senko/tornado-proxy
class LocalProxyHandler(IPythonHandler):
    proxy_uri = "http://localhost"

    @tornado.web.asynchronous
    def get(self, port, add_path=''):
        logger.info('%s request to %s', self.request.method, self.request.uri)

        def handle_response(response):
            if (response.error and not
                    isinstance(response.error, tornado.httpclient.HTTPError)):
                self.set_status(500)
                self.write('Internal server error:\n' + str(response.error))
            else:
                self.set_status(response.code, response.reason)
                # clear tornado default header
                self._headers = tornado.httputil.HTTPHeaders()
                
                for header, v in response.headers.get_all():
                    if header not in ('Content-Length', 'Transfer-Encoding',
                        'Content-Encoding', 'Connection'):
                        # some header appear multiple times, eg 'Set-Cookie'
                        self.add_header(header, v)
                
                if response.body:                   
                    self.set_header('Content-Length', len(response.body))
                    self.write(response.body)

            self.finish()

        if 'Proxy-Connection' in self.request.headers:
            del self.request.headers['Proxy-Connection'] 

        body = self.request.body
        if not body: body = None

        # self.request.uri is /user/username/port/([0-9]+)/something and
        # we need to strip off the first four elements.
        new_path = '/'.join(self.request.uri.split('/')[5:])
        if new_path != '': new_path = '/' + new_path
        uri = self.proxy_uri + ':' + port + new_path
        client = tornado.httpclient.AsyncHTTPClient()

        try:
            logger.info('Requesting %s', uri)
            req = tornado.httpclient.HTTPRequest(
                uri, method=self.request.method, body=body,
                headers=self.request.headers, follow_redirects=False)
            client.fetch(req, handle_response, raise_error=False)
        except tornado.httpclient.HTTPError as e:
            if hasattr(e, 'response') and e.response:
                handle_response(e.response)
            else:
                self.set_status(500)
                self.write('Internal server error:\n' + str(e))
                self.finish()

def setup_handlers(web_app):
    host_pattern = '.*$'
    for p in ['/proxy/([0-9]+)/?','/proxy/([0-9]+)/(.*)']:
        route_pattern = url_path_join(web_app.settings['base_url'], p)
        web_app.add_handlers(host_pattern, [
            (route_pattern, LocalProxyHandler),
        ])
    logger.info('Added handler for route %s', route_pattern)
