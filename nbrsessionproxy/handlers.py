# vim: set et sw=4 ts=4:
import os
import getpass
import pwd
import tempfile

from urllib.parse import urlunparse, urlparse

from tornado import web

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


class RSessionProxyHandler(SuperviseAndProxyHandler):
    '''Manage an RStudio rsession instance.'''

    name = 'rsession'

    def get_env(self):
        env = {}

        # rserver needs USER to be set to something sensible,
        # otherwise it'll throw up an authentication page
        if not os.environ.get('USER', ''):
            env['USER'] = getpass.getuser()

        return env

    def get_cmd(self):
        # rsession command. Augmented with user-identity and www-port.
        return [
            'rserver',
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
