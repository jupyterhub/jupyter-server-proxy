import os
import json
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

# from jupyterhub.utils
def random_port():
    """get a single random port"""
    sock = socket.socket()
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port

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

    def rsession_uri(self):
        return '{}proxy/{}/'.format(self.base_url, self.state['port'])

    def gen_response(self, proc):
        response = {
            'pid': proc.pid,
            'url':self.rsession_uri(),
        }
        return response
        
    def get_client_id(self):
        '''Returns either None or the value of 'active-client-id' from
           ~/.rstudio/session-persistent-state.'''

        client_id = None

        # Assume the contents manager is local
        #root_dir = self.settings['contents_manager'].root_dir
        #root_dir = self.config.FileContentsManager.root_dir
        root_dir = os.getcwd()

        self.log.debug('client_id: root_dir: {}'.format(root_dir))
        path = os.path.join(root_dir, '.rstudio', 'session-persistent-state')
        if not os.path.exists(path):
            self.log.debug('client_id: No such file: {}'.format(path))
            return client_id

        try:
            buf = open(path).read()
        except Exception as e:
            self.log.debug("client_id: could not read {}: {}".format(path, e))
            return client_id

        self.log.debug("client_id: read {} bytes".format(len(buf)))
        config_key = 'active-client-id'
        for line in buf.split():
            if line.startswith(config_key + '='):
                # remove the key, '=', and leading and trailing quotes
                client_id = line[len(config_key)+1+1:-1]
                self.log.debug('client_id: read: {}'.format(client_id))
                break

        return client_id 
        
    def is_running(self):
        '''Check if our proxied process is still running.'''

        if 'proc' not in self.state:
            return False
        elif 'port' not in self.state:
            return False

        # Check if the process is still around
        proc = self.state['proc']
        if proc.poll() == 0:
            del(self.state['proc'])
            self.log.debug('Cannot poll on process.')
            return False
        
        # Check if it is still bound to the port
        port = self.state['port']
        sock = socket.socket()
        try:
            self.log.debug('Binding on port {}.'.format(port))
            sock.bind(('', port))
        except OSError as e:
            self.log.debug('Bind error: {}'.format(str(e)))
            if e.strerror != 'Address already in use':
                return False

        sock.close()

        return True

    def is_available(self):
        pass

    def rpc(self, path):
        clientid = self.get_client_id()
        if not clientid:
            return False

        uri = self.rsession_uri()
        
        
    @web.authenticated
    def post(self):
        '''Start a new rsession.'''

        if self.is_running():
            proc = self.state['proc']
            port = self.state['port']
            self.log.info('Resuming process on port {}'.format(port))
            response = self.gen_response(proc)
            self.finish(json.dumps(response))
            return

        self.log.debug('No existing process')

        username = os.environ.get('JPY_USER', default='jovyan')
        port = random_port()

        cmd = self.cmd + [
            '--user-identity=' + username,
            '--www-port=' + str(port)
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
                sock.connect(('', port))
                break
            except socket.error as e:
                print('sleeping: {}'.format(e))
                time.sleep(2)
                rsession_attempts += 1

        # Store our process
        self.state['proc'] = proc
        self.state['port'] = port

        response = self.gen_response(proc)

        client_id = self.get_client_id()
        self.log.debug('post: client_id: {}'.format(client_id))
        self.finish(json.dumps(response))

    @web.authenticated
    def get(self):
        if self.is_running():
            proc = self.state['proc']
            port = self.state['port']
            self.log.info('Process exists on port {}'.format(port))
            response = self.gen_response(proc)
            self.finish(json.dumps(response))
            return
        self.finish(json.dumps({}))
 
    @web.authenticated
    def delete(self):
        if 'proc' not in self.state:
            raise web.HTTPError(reason='no rsession running', status_code=500)
        proc = self.state['proc']
        proc.kill()
        self.finish()

def setup_handlers(web_app):
    host_pattern = '.*$'
    route_pattern = ujoin(web_app.settings['base_url'], '/rsessionproxy/?')
    web_app.add_handlers(host_pattern, [
        (route_pattern, RSessionProxyHandler, dict(state=state_data))
    ])

# vim: set et ts=4 sw=4:
