from __future__ import annotations

from logging import Logger

from jupyter_server.utils import ensure_async
from jupyterhub import __version__ as __jh_version__
from jupyterhub.services.auth import HubOAuthenticated
from tornado import web
from tornado.log import app_log
from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler

from ..handlers import SuperviseAndProxyHandler


class StandaloneHubProxyHandler(HubOAuthenticated, SuperviseAndProxyHandler):
    """
    Base class for standalone proxies.
    Will restrict access to the application by authentication with the JupyterHub API.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.environment = {}
        self.timeout = 60
        self.skip_authentication = False

    @property
    def log(self) -> Logger:
        return app_log

    @property
    def hub_users(self):
        if "hub_user" in self.settings:
            return {self.settings["hub_user"]}
        return set()

    @property
    def hub_groups(self):
        if "hub_group" in self.settings:
            return {self.settings["hub_group"]}
        return set()

    def set_default_headers(self):
        self.set_header("X-JupyterHub-Version", __jh_version__)

    def prepare(self, *args, **kwargs):
        pass

    def check_origin(self, origin: str = None):
        # Skip JupyterHandler.check_origin
        return WebSocketHandler.check_origin(self, origin)

    def check_xsrf_cookie(self):
        # Skip HubAuthenticated.check_xsrf_cookie
        pass

    def write_error(self, status_code: int, **kwargs):
        # ToDo: Return proper error page, like in jupyter-server/JupyterHub
        return RequestHandler.write_error(self, status_code, **kwargs)

    async def proxy(self, port, path):
        if self.skip_authentication:
            return await super().proxy(port, path)
        else:
            return await ensure_async(self.oauth_proxy(port, path))

    @web.authenticated
    async def oauth_proxy(self, port, path):
        return await super().proxy(port, path)

    def get_env(self):
        return self._render_template(self.environment)

    def get_timeout(self):
        return self.timeout


def make_proxy(
    command, port, unix_socket, environment, mappath, timeout, skip_authentication
) -> tuple[type, dict]:
    class Proxy(StandaloneHubProxyHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.name = f"{command[0]!r} Process"
            self.proxy_base = command[0]
            self.requested_port = port
            self.requested_unix_socket = unix_socket
            self.mappath = mappath
            self.command = command
            self.environment = environment
            self.timeout = timeout
            self.skip_authentication = skip_authentication

    return Proxy, dict(state={})
