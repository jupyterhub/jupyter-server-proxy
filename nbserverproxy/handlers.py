"""
Authenticated HTTP proxy for Jupyter Notebooks

Some original inspiration from https://github.com/senko/tornado-proxy
"""
import socket
import os
from tornado import gen, web, httpclient, httputil, process

from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler


class LocalProxyHandler(IPythonHandler):
    proxy_uri = "http://localhost"

    @web.authenticated
    @gen.coroutine
    def proxy(self, port, proxied_path):
        '''
        While self.request.uri is
            (hub)    /user/username/proxy/([0-9]+)/something.
            (single) /proxy/([0-9]+)/something
        This serverextension is given {port}/{everything/after}.
        '''

        if 'Proxy-Connection' in self.request.headers:
            del self.request.headers['Proxy-Connection']

        body = self.request.body
        if not body:
            body = None

        client_uri = '{uri}:{port}{path}'.format(
            uri=self.proxy_uri,
            port=port,
            path=proxied_path
        )
        if self.request.query:
            client_uri += '?' + self.request.query

        client = httpclient.AsyncHTTPClient()

        req = httpclient.HTTPRequest(
            client_uri, method=self.request.method, body=body,
            headers=self.request.headers, follow_redirects=False)

        response = yield client.fetch(req, raise_error=False)

        # For all non http errors...
        if response.error and type(response.error) is not httpclient.HTTPError:
            self.set_status(500)
            self.write(str(response.error))
        else:
            self.set_status(response.code, response.reason)

            # clear tornado default header
            self._headers = httputil.HTTPHeaders()

            for header, v in response.headers.get_all():
                if header not in ('Content-Length', 'Transfer-Encoding',
                    'Content-Encoding', 'Connection'):
                    # some header appear multiple times, eg 'Set-Cookie'
                    self.add_header(header, v)


            if response.body:
                self.write(response.body)

    # support all the methods that torando does by default!
    def get(self, port, proxy_path=''):
        return self.proxy(port, proxy_path)

    def post(self, port, proxy_path=''):
        return self.proxy(port, proxy_path)

    def put(self, port, proxy_path=''):
        return self.proxy(port, proxy_path)

    def delete(self, port, proxy_path=''):
        return self.proxy(port, proxy_path)

    def head(self, port, proxy_path=''):
        return self.proxy(port, proxy_path)

    def patch(self, port, proxy_path=''):
        return self.proxy(port, proxy_path)

    def options(self, port, proxy_path=''):
        return self.proxy(port, proxy_path)

    def check_xsrf_cookie(self):
        '''
        http://www.tornadoweb.org/en/stable/guide/security.html

        Defer to proxied apps.
        '''
        pass


class SuperviseAndProxyHandler(LocalProxyHandler):
    '''Manage a given process and requests to it '''

    def initialize(self, state):
        self.state = state

    name = 'process'

    @property
    def port(self):
        """
        Allocate a random empty port for use by rstudio
        """
        if 'port' not in self.state:
            sock = socket.socket()
            sock.bind(('', 0))
            self.state['port'] = sock.getsockname()[1]
            sock.close()
        return self.state['port']

    @gen.coroutine
    def is_running(self, proc):
        '''Check if our proxied process is still running.'''

        # Check if the process is still around
        if proc.proc.poll() == 0:
            self.log.info('Poll failed for', self.name)
            return False

        client = httpclient.AsyncHTTPClient()
        req = httpclient.HTTPRequest('http://localhost:{}'.format(self.port))

        try:
            yield client.fetch(req)
            self.log.debug('Got positive response from proxied', self.name)
        except:
            self.log.debug('Got negative response from proxied', self.name)
            return False

        return True


    @gen.coroutine
    def start_process(self):
        """
        Start the rstudio process
        """
        if 'starting' in self.state:
            raise Exception("Process {} start already pending, can not start again".format(self.name))
        if 'proc' in self.state:
            raise Exception("Process {} already running, can not start".format(self.name))
        self.state['starting'] = True
        cmd = self.get_cmd()

        server_env = os.environ.copy()

        # Seed RStudio's R and RSTUDIO env variables
        server_env.update(self.get_env())

        @gen.coroutine
        def exit_callback(code):
            """
            Callback when the process dies
            """
            self.log.info('{} died with code {}'.format(self.name, code))
            del self.state['proc']
            if code != 0 and not 'starting' in self.state:
                yield self.start_process()

        # Runs rsession in background
        proc = process.Subprocess(cmd, env=server_env)
        self.log.info('Starting process...')
        proc.set_exit_callback(exit_callback)

        for i in range(5):
            if (yield self.is_running(proc)):
                self.log.info('{} startup complete'.format(self.name))
                break
            # Simple exponential backoff
            wait_time = max(1.4 ** i, 5)
            self.log.debug('Waiting {} before checking if {} is up'.format(wait_time, self.name))
            yield gen.sleep(wait_time)
        else:
            raise web.HTTPError('could not start {} in time'.format(self.name), status_code=500)

        # add proc to state only after we are sure it has started
        self.state['proc'] = proc

        del self.state['starting']

    @gen.coroutine
    @web.authenticated
    def proxy(self, port, path):
        if not path.startswith('/'):
            path = '/' + path

        if 'starting' in self.state:
            self.log.info('{} already starting, waiting for it to start...'.format(self.name))
            for i in range(5):
                if 'proc' in self.state:
                    self.log.info('{} startup complete'.format(self.name))
                    break
                # Simple exponential backoff
                wait_time = max(1.4 ** i, 5)
                self.log.debug('Waiting {} before checking if process is up'.format(wait_time))
                yield gen.sleep(wait_time)
            else:
                raise web.HTTPError('{} did not start in time'.format(self.name), status_code=500)
        else:
            if 'proc' not in self.state:
                self.log.info('No existing {} found'.format(self.name))
                yield self.start_process()

        return (yield super().proxy(self.port, path))

    def get(self, path):
        return self.proxy(self.port, path)

    def post(self, path):
        return self.proxy(self.port, path)

    def put(self, path):
        return self.proxy(self.port, path)

    def delete(self, path):
        return self.proxy(self.port, path)

    def head(self, path):
        return self.proxy(self.port, path)

    def patch(self, path):
        return self.proxy(self.port, path)

    def options(self, path):
        return self.proxy(self.port, path)

def setup_handlers(web_app):
    host_pattern = '.*$'
    web_app.add_handlers('.*', [
        (url_path_join(web_app.settings['base_url'], r'/proxy/(\d+)(.*)'), LocalProxyHandler)
    ])
#vim: set et ts=4 sw=4:
