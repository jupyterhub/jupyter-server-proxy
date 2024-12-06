import os
import re
from logging import Logger

from jupyterhub import __version__ as __jh_version__
from jupyterhub.services.auth import HubOAuthCallbackHandler, HubOAuthenticated
from jupyterhub.utils import make_ssl_context
from tornado import httpclient, web
from tornado.log import app_log
from tornado.web import Application
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

    async def proxy(self, port, path):
        if self.skip_authentication:
            return await super().proxy(port, path)
        else:
            return await self.oauth_proxy(port, path)

    @web.authenticated
    async def oauth_proxy(self, port, path):
        return await super().proxy(port, path)

    def check_origin(self, origin: str = None):
        # Skip JupyterHandler.check_origin
        return WebSocketHandler.check_origin(self, origin)

    def get_env(self):
        return self._render_template(self.environment)

    def get_timeout(self):
        return self.timeout


def configure_ssl():
    keyfile = os.environ.get("JUPYTERHUB_SSL_KEYFILE")
    certfile = os.environ.get("JUPYTERHUB_SSL_CERTFILE")
    cafile = os.environ.get("JUPYTERHUB_SSL_CLIENT_CA")

    if not (keyfile and certfile and cafile):
        app_log.warn("Could not configure SSL")
        return None

    ssl_context = make_ssl_context(keyfile, certfile, cafile)

    # Configure HTTPClient to use SSL for Proxy Requests
    httpclient.AsyncHTTPClient.configure(None, defaults={"ssl_options": ssl_context})

    return ssl_context


def make_proxy_app(
    command: list[str],
    prefix: str,
    port: int,
    unix_socket: bool | str,
    environment: dict[str, str],
    mappath: dict[str, str],
    timeout: int,
    skip_authentication: bool,
    debug: bool,
    # progressive: bool,
    websocket_max_message_size: int,
):
    app_log.debug(f"Process will use {port = }")
    app_log.debug(f"Process will use {unix_socket = }")
    app_log.debug(f"Process environment: {environment}")
    app_log.debug(f"Proxy mappath: {mappath}")

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

    settings = dict(
        debug=debug,
        # Required for JupyterHub
        hub_user=os.environ.get("JUPYTERHUB_USER", ""),
        hub_group=os.environ.get("JUPYTERHUB_GROUP", ""),
        cookie_secret=os.urandom(32),
    )

    if websocket_max_message_size:
        app_log.debug(f"Restricting WebSocket Messages to {websocket_max_message_size}")
        settings["websocket_max_message_size"] = websocket_max_message_size

    app = Application(
        [
            (
                r"^" + re.escape(prefix) + r"/(.*)",
                Proxy,
                dict(
                    state={},
                    # ToDo: progressive=progressive
                ),
            ),
            (
                r"^" + re.escape(prefix) + r"/oauth_callback",
                HubOAuthCallbackHandler,
            ),
        ],
        **settings,
    )

    return app
