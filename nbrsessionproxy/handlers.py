# vim: set et sw=4 ts=4:
import os
import getpass
import pwd
import tempfile

from urllib.parse import urlunparse, urlparse

from tornado import web
import subprocess

from notebook.utils import url_path_join as ujoin
from notebook.base.handlers import IPythonHandler

from nbserverproxy.handlers import SuperviseAndProxyHandler


class AddSlashHandler(IPythonHandler):
    """Handler for adding trailing slash to URLs that need them"""
    @web.authenticated
    def get(self, *args):
        src = urlparse(self.request.uri)
        dest = src._replace(path=src.path + '/')
        self.redirect(urlunparse(dest))

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



class RSessionProxyHandler(SuperviseAndProxyHandler):
    '''Manage an RStudio rsession instance.'''

    name = 'rsession'

    def get_env(self):
        env = {}
        try:
            r_vars = detectR()
            env.update(r_vars)
        except:
            raise web.HTTPError(reason='could not detect R', status_code=500)

        # rserver needs USER to be set to something sensible,
        # otherwise it'll throw up an authentication page
        if not os.environ.get('USER', ''):
            env['USER'] = getpass.getuser()

        return env

    def get_cmd(self):
        # rsession command. Augmented with user-identity and www-port.
        return [
            'rsession',
            '--standalone=1',
            '--program-mode=server',
            '--log-stderr=1',
            '--session-timeout-minutes=0',
            '--user-identity=' + getpass.getuser(),
            '--www-port=' + str(self.port)
        ]

class ShinyProxyHandler(SuperviseAndProxyHandler):
    '''Manage a Shiny instance.'''

    name = 'shiny'
    conf_tmpl = """run_as {user};
server {{
  listen {port};
  location / {{
    site_dir {site_dir};
    log_dir {site_dir}/logs;
    directory_index on;
  }}
}}
"""

    def write_conf(self, user, port, site_dir):
        '''Create a configuration file and return its name.'''
        conf = self.conf_tmpl.format(user=user, port=port, site_dir=site_dir)
        f = tempfile.NamedTemporaryFile(mode='w', delete=False)
        f.write(conf)
        f.close()
        return f.name

    def get_env(self):
        return {}

    def get_cmd(self):
        user = getpass.getuser()
        site_dir = pwd.getpwnam(user).pw_dir
        filename = self.write_conf(user, self.port, site_dir)

        # shiny command.
        return [ 'shiny-server', filename ] 

def setup_handlers(web_app):
    web_app.add_handlers('.*', [
        (ujoin(web_app.settings['base_url'], 'rstudio/(.*)'), RSessionProxyHandler, dict(state={})),
        (ujoin(web_app.settings['base_url'], 'shiny/(.*)'),   ShinyProxyHandler, dict(state={})),
        (ujoin(web_app.settings['base_url'], 'rstudio'), AddSlashHandler),
        (ujoin(web_app.settings['base_url'], 'shiny'),   AddSlashHandler)
    ])
