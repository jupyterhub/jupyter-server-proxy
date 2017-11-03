import os
import json
import getpass
import socket
import time
import subprocess as sp

from tornado import web

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

# Data shared between handler requests
state_data = dict()

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
        self.port = 9797

    def rsession_uri(self):
        return '{}proxy/{}/'.format(self.base_url, self.port)

    def is_running(self):
        '''Check if our proxied process is still running.'''

        if 'proc' not in self.state:
            return False

        # Check if the process is still around
        proc = self.state['proc']
        if proc.poll() == 0:
            del(self.state['proc'])
            self.log.debug('Cannot poll on process.')
            return False

        # Check if it is still bound to the port
        sock = socket.socket()
        try:
            self.log.debug('Binding on port {}.'.format(self.port))
            sock.bind(('', self.port))
        except OSError as e:
            self.log.debug('Bind error: {}'.format(str(e)))
            if e.strerror != 'Address already in use':
                return False

        sock.close()

        return True


    @web.authenticated
    def get(self):
        '''Start a new rsession.'''

        if self.is_running():
            proc = self.state['proc']
            self.log.info('Resuming process on port {}'.format(self.port))
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
            self.finish()

        # Runs rsession in background
        proc = sp.Popen(cmd, env=server_env)

        if proc.poll() == 0:
            raise web.HTTPError(reason='rsession terminated', status_code=500)
            self.finish()

        # Wait for rsession to be available
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rsession_attempts = 0
        while rsession_attempts < 5:
            try:
                sock.connect(('', self.port))
                break
            except socket.error as e:
                print('sleeping: {}'.format(e))
                time.sleep(2)
                rsession_attempts += 1

        # Store our process
        self.state['proc'] = proc

        return self.redirect(self.rsession_uri())

def setup_handlers(web_app):
    host_pattern = '.*$'
    route_pattern = ujoin(web_app.settings['base_url'], '/rsessionproxy/?')
    web_app.add_handlers(host_pattern, [
        (route_pattern, RSessionProxyHandler, dict(state=state_data))
    ])

# vim: set et ts=4 sw=4:
