import os
import getpass
import socket
import subprocess
from urllib.parse import urlunparse, urlparse

from tornado import web, gen, httpclient, process, ioloop

from notebook.utils import url_path_join as ujoin
from notebook.base.handlers import IPythonHandler

from nbserverproxy.handlers import LocalProxyHandler


def detectR():
    '''Detect R's version, R_HOME, and various other directories that rsession
       requires.

       Via rstudio's src/cpp/core/r_util/REnvironmentPosix.cpp'''

    cmd = ['R', '--slave', '--vanilla', '-e',
             'cat(paste(R.home("home"),R.home("share"),R.home("include"),R.home("doc"),getRversion(),sep=":"))']

    p = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        raise Exception('Error detecting R')
    R_HOME, R_SHARE_DIR, R_INCLUDE_DIR, R_DOC_DIR, version = \
        p.stdout.decode().split(':')

    return {
        'R_DOC_DIR': R_DOC_DIR,
        'R_HOME': R_HOME,
        'R_INCLUDE_DIR': R_INCLUDE_DIR,
        'R_SHARE_DIR': R_SHARE_DIR,
        'RSTUDIO_DEFAULT_R_VERSION_HOME': R_HOME,
        'RSTUDIO_DEFAULT_R_VERSION': version,
    }

class AddSlashHandler(IPythonHandler):
    """Handler for adding trailing slash to URLs that need them"""
    @web.authenticated
    def get(self, *args):
        src = urlparse(self.request.uri)
        dest = src._replace(path=src.path + '/')
        self.redirect(urlunparse(dest))

class RSessionProxyHandler(LocalProxyHandler):
    '''Manage an RStudio rsession instance.'''

    # R and RStudio environment variables required by rsession.
    env = {
        'RSTUDIO_LIMIT_RPC_CLIENT_UID':'998', 
        'RSTUDIO_MINIMUM_USER_ID':'500', 
    }

    # rsession command. Augmented with user-identity and www-port.
    cmd = [
        'rsession',
        '--standalone=1',
        '--program-mode=server',
        '--log-stderr=1',
        '--session-timeout-minutes=0',
    ]


    def initialize(self, state):
        self.state = state

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

    def rsession_uri(self):
        return '{}proxy/{}/'.format(self.base_url, self.port)

    @gen.coroutine
    def is_running(self):
        '''Check if our proxied process is still running.'''

        if 'proc' not in self.state:
            return False

        # Check if the process is still around
        proc = self.state['proc']
        if proc.proc.poll() == 0:
            self.log.info('Cannot poll on process.')
            return False

        client = httpclient.AsyncHTTPClient()
        req = httpclient.HTTPRequest('http://localhost:{}'.format(self.port))

        try:
            yield client.fetch(req)
            self.log.debug('Got positive response from rstudio server')
        except:
            self.log.debug('Got negative response from rstudio server')
            return False

        return True


    @gen.coroutine
    def start_process(self):
        """
        Start the rstudio process
        """

        self.state['starting'] = True
        try:
            cmd = self.cmd + [
                '--user-identity=' + getpass.getuser(),
                '--www-port=' + str(self.port)
            ]

            server_env = os.environ.copy()

            # Seed RStudio's R and RSTUDIO env variables
            server_env.update(self.env)

            try:
                r_vars = detectR()
                server_env.update(r_vars)
            except:
                raise web.HTTPError(reason='could not detect R', status_code=500)

            @gen.coroutine
            def exit_callback(code):
                """
                Callback when the rsessionproxy dies
                """
                self.log.info('rsession process died with code {}'.format(code))
                del self.state['proc']
                if code != 0:
                    yield self.start_process()

            # Runs rsession in background
            proc = process.Subprocess(cmd, env=server_env)
            self.log.info('Starting rsession process...')
            self.state['proc'] = proc
            proc.set_exit_callback(exit_callback)

            for i in range(5):
                if (yield self.is_running()):
                    self.log.info('rsession startup complete')
                    break
                # Simple exponential backoff
                wait_time = max(1.4 ** i, 5)
                self.log.debug('Waiting {} before checking if rstudio is up'.format(wait_time))
                yield gen.sleep(wait_time)
            else:
                raise web.HTTPError('could not start rsession in time', status_code=500)
        finally:
            self.state['starting'] = False


    @gen.coroutine
    @web.authenticated
    def proxy(self, port, path):
        if not path.startswith('/'):
            path = '/' + path

        # if we're in 'starting' let's wait a while
        for i in range(5):
            if not self.state.get('starting', False):
                break
            # Simple exponential backoff
            wait_time = max(1.4 ** i, 5)
            self.log.debug('Waiting {} before checking if rstudio is up'.format(wait_time))
            yield gen.sleep(wait_time)
        else:
            raise web.HTTPError('could not start rsession in time', status_code=500)

        # FIXME: try to not start multiple processes at a time with some locking here
        if 'proc' not in self.state:
            self.log.info('No existing process rsession process found')
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
    web_app.add_handlers('.*', [
        (ujoin(web_app.settings['base_url'], 'rstudio/(.*)'), RSessionProxyHandler, dict(state={})),
        (ujoin(web_app.settings['base_url'], 'rstudio'), AddSlashHandler)
    ])

# vim: set et ts=4 sw=4:
