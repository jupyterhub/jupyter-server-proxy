import os
import json
import logging
import socket
import subprocess as sp

from tornado import web

from traitlets import List, Dict

from notebook.utils import url_path_join as ujoin
from notebook.base.handlers import IPythonHandler

logger = logging.getLogger('nbrsessionproxy')

# from jupyterhub.utils
def random_port():
    """get a single random port"""
    sock = socket.socket()
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port

class RSessionProxyHandler(IPythonHandler):
    '''Manage an RStudio rsession instance.'''

    # rsession's environment will vary depending on how it was compiled.
    # Configure the env and cmd as required; values here work on Ubuntu.

    rsession_paths = Dict({
        'PATH':'/usr/local/sbin:/usr/local/bin:/usr/bin:/usr/sbin:/sbin:/bin',
        'LD_LIBRARY_PATH':'/usr/lib/R/lib:/lib:/usr/lib/x86_64-linux-gnu:/usr/lib/jvm/java-7-openjdk-amd64/jre/lib/amd64/server'
    })

    rsession_env = Dict({
        'R_DOC_DIR':'/usr/share/R/doc', 
        'R_HOME':'/usr/lib/R', 
        'R_INCLUDE_DIR':'/usr/share/R/include', 
        'R_SHARE_DIR':'/usr/share/R/share', 
        'RSTUDIO_DEFAULT_R_VERSION':'3.3.0', 
        'RSTUDIO_DEFAULT_R_VERSION_HOME':'/usr/lib/R', 
        'RSTUDIO_LIMIT_RPC_CLIENT_UID':'998', 
        'RSTUDIO_MINIMUM_USER_ID':'500', 
    })

    # This command will be added to later on POST
    rsession_cmd = List([
        '/usr/lib/rstudio-server/bin/rsession',
        '--standalone=1',
        '--program-mode=server',
        '--log-stderr=1',
        '--session-timeout-minutes=0',
    ])

    port = random_port()

    proc = None

    @web.authenticated
    def post(self):
        logger.info('%s request to %s', self.request.method, self.request.uri)

        cmd = self.rsession_cmd + [
            '--user-identity=' + self.current_user,
            '--www-port=' + str(self.port)
        ]

        server_env = os.environ.copy()

        # Seed RStudio's R and RSTUDIO variables
        server_env.update(self.rsession_env)

        # Prepend RStudio's requisite paths
        for env_var in self.rsession_paths.keys():
            path = server_env.get(env_var, '')
            if path != '': path = ':' + path
            server_env[env_var] = self.rsession_paths[env_var] + path

        # Runs rsession in background since we do not need stdout/stderr
        self.proc = sp.Popen(cmd, env=server_env)

        if self.proc.poll() == 0:
            raise web.HTTPError(reason='rsession terminated', status_code=500)
            self.finish()

        response = {
            'pid':self.proc.pid,
            'url':'{}proxy/{}/'.format(self.base_url, self.port),
        }

        self.finish(json.dumps(response))

    @web.authenticated
    def get(self):
        if not self.proc:
            raise web.HTTPError(reason='rsession not yet started', status_code=500)
        self.finish(self.proc.poll())
 
    def delete(self):
        logger.info('%s request to %s', self.request.method, self.request.uri)
        self.proc.kill()
        self.finish(self.proc.poll())

def setup_handlers(web_app):
    host_pattern = '.*$'
    route_pattern = ujoin(web_app.settings['base_url'], '/rsessionproxy/?')
    web_app.add_handlers(host_pattern, [
        (route_pattern, RSessionProxyHandler)
    ])
    logger.info('Added handler for route %s', route_pattern)

# vim: set et ts=4 sw=4:
