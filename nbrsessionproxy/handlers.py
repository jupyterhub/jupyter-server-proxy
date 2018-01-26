import os
import getpass
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

def setup_handlers(web_app):
    web_app.add_handlers('.*', [
        (ujoin(web_app.settings['base_url'], 'rstudio/(.*)'), RSessionProxyHandler, dict(state={})),
        (ujoin(web_app.settings['base_url'], 'rstudio'), AddSlashHandler)
    ])
