import os
import json
import socket
import subprocess as sp

from tornado import web

from traitlets import List, Dict
from traitlets.config import Configurable

from notebook.utils import url_path_join as ujoin
from notebook.base.handlers import IPythonHandler

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

class RSessionContext(Configurable):

    # rsession's environment will vary depending on how it was compiled.
    # Configure the env and cmd as required; values here work on Ubuntu.

    paths = Dict({
        'PATH':'/usr/local/sbin:/usr/local/bin:/usr/bin:/usr/sbin:/sbin:/bin',
        'LD_LIBRARY_PATH':'/usr/lib/R/lib:/lib:/usr/lib/x86_64-linux-gnu:/usr/lib/jvm/java-7-openjdk-amd64/jre/lib/amd64/server'
    }, help="Executable and dynamic linker paths required by rsession.")

    env = Dict({
        'R_DOC_DIR':'/usr/share/R/doc', 
        'R_HOME':'/usr/lib/R', 
        'R_INCLUDE_DIR':'/usr/share/R/include', 
        'R_SHARE_DIR':'/usr/share/R/share', 
        'RSTUDIO_DEFAULT_R_VERSION':'3.3.0', 
        'RSTUDIO_DEFAULT_R_VERSION_HOME':'/usr/lib/R', 
        'RSTUDIO_LIMIT_RPC_CLIENT_UID':'998', 
        'RSTUDIO_MINIMUM_USER_ID':'500', 
    }, help="R and RStudio environment variables required by rsession.")

    cmd = List([
        '/usr/lib/rstudio-server/bin/rsession',
        '--standalone=1',
        '--program-mode=server',
        '--log-stderr=1',
        '--session-timeout-minutes=0',
    ], help="rsession command. Augmented with user-identity and www-port")

class RSessionProxyHandler(IPythonHandler):
    '''Manage an RStudio rsession instance.'''

    rsession_context = RSessionContext()

    def initialize(self, state):
        self.state = state

    def gen_response(self, proc, port):
        response = {
            'pid': proc.pid,
            'url':'{}proxy/{}/'.format(self.base_url, port),
        }
        return response
        
    def still_running(self):
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
        port = self.state['port']
        sock = socket.socket()
        try:
            self.log.debug('Binding on port {}.'.format(port))
            sock.bind(('', port))
        except OSError as e:
            self.log.debug('Bind error: {}'.format(str(e)))
            return True
        else:
            sock.close()
        del(self.state['port'])

        return False

    @web.authenticated
    def post(self):
        '''Start a new rsession.'''

        if self.still_running():
            proc = self.state['proc']
            port = self.state['port']
            self.log.info('Resuming process on port {}'.format(port))
            response = self.gen_response(proc, port)
            self.finish(json.dumps(response))
            return

        self.log.debug('No existing process')
        port = random_port()

        cmd = self.rsession_context.cmd + [
            '--user-identity=' + self.current_user,
            '--www-port=' + str(port)
        ]

        server_env = os.environ.copy()

        # Seed RStudio's R and RSTUDIO env variables
        server_env.update(self.rsession_context.env)

        # Prepend RStudio's requisite paths
        for env_var in self.rsession_context.paths.keys():
            path = server_env.get(env_var, '')
            if path != '': path = ':' + path
            server_env[env_var] = self.rsession_context.paths[env_var] + path

        # Runs rsession in background
        proc = sp.Popen(cmd, env=server_env)

        if proc.poll() == 0:
            raise web.HTTPError(reason='rsession terminated', status_code=500)
            self.finish()

        response = self.gen_response(proc, port)

        # Store our process
        self.state['proc'] = proc
        self.state['port'] = port

        self.finish(json.dumps(response))

    @web.authenticated
    def get(self):
        if 'proc' not in self.state:
            raise web.HTTPError(reason='no rsession running', status_code=500)
        proc = self.state['proc']
        self.finish(str(proc.pid))
 
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
