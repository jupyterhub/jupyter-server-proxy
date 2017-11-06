import os
import getpass
import socket
import subprocess as sp

from tornado import web, gen, httpclient

from notebook.utils import url_path_join as ujoin
from notebook.base.handlers import IPythonHandler


def detectR():
    '''Detect R's version, R_HOME, and various other directories that rsession
       requires.

       Via rstudio's src/cpp/core/r_util/REnvironmentPosix.cpp'''

    cmd = ['R', '--slave', '--vanilla', '-e',
             'cat(paste(R.home("home"),R.home("share"),R.home("include"),R.home("doc"),getRversion(),sep=":"))']

    p = sp.run(cmd, check=True, stdout=sp.PIPE, stderr=sp.PIPE)
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


class RSessionProxyHandler(IPythonHandler):
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
        if not hasattr(self, '_port'):
            sock = socket.socket()
            sock.bind(('', 0))
            self._port = sock.getsockname()[1]
            sock.close()
        return self._port

    def rsession_uri(self):
        return '{}proxy/{}/'.format(self.base_url, self.port)

    @gen.coroutine
    def is_running(self):
        '''Check if our proxied process is still running.'''

        if 'proc' not in self.state:
            return False

        # Check if the process is still around
        proc = self.state['proc']
        if proc.poll() == 0:
            self.log.debug('Cannot poll on process.')
            return False

        client = httpclient.AsyncHTTPClient()
        req = httpclient.HTTPRequest('http://localhost:{}'.format(self.port))

        try:
            yield client.fetch(req)
            self.log.debug('Got positive response from rstudio server')
        except:
            return False

        return True


    @gen.coroutine
    @web.authenticated
    def get(self):
        '''Start a new rsession.'''

        if (yield self.is_running()):
            self.log.info('R process on port {}'.format(self.port))
            return self.redirect(self.rsession_uri())

        self.log.debug('No existing process')

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

        # Runs rsession in background
        proc = sp.Popen(cmd, env=server_env)
        self.state['proc'] = proc

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

        return self.redirect(self.rsession_uri())

def setup_handlers(web_app):
    route_pattern = ujoin(web_app.settings['base_url'], '/rstudio/?')
    web_app.add_handlers('.*', [
        (route_pattern, RSessionProxyHandler, dict(state={}))
    ])

# vim: set et ts=4 sw=4:
