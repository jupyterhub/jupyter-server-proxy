from __future__ import annotations

import os
import re
import ssl
from logging import Logger

from jupyter_server.utils import ensure_async
from jupyterhub import __version__ as __jh_version__
from jupyterhub.services.auth import HubOAuthCallbackHandler, HubOAuthenticated
from jupyterhub.utils import make_ssl_context
from tornado import httpclient, web
from tornado.log import app_log
from tornado.web import Application, RedirectHandler, RequestHandler
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


def configure_ssl():
    # See https://github.com/jupyter-server/jupyter_server/blob/v2.0.0/jupyter_server/serverapp.py#L2053-L2073
    keyfile = os.environ.get("JUPYTERHUB_SSL_KEYFILE", "")
    certfile = os.environ.get("JUPYTERHUB_SSL_CERTFILE", "")
    client_ca = os.environ.get("JUPYTERHUB_SSL_CLIENT_CA", "")

    if not (keyfile or certfile or client_ca):
        app_log.warn("Could not configure SSL")
        return None

    ssl_options = {}
    if keyfile:
        ssl_options["keyfile"] = keyfile
    if certfile:
        ssl_options["certfile"] = certfile
    if client_ca:
        ssl_options["ca_certs"] = client_ca

    # PROTOCOL_TLS selects the highest ssl/tls protocol version that both the client and
    # server support. When PROTOCOL_TLS is not available use PROTOCOL_SSLv23.
    ssl_options["ssl_version"] = getattr(ssl, "PROTOCOL_TLS", ssl.PROTOCOL_SSLv23)
    if ssl_options.get("ca_certs", False):
        ssl_options["cert_reqs"] = ssl.CERT_REQUIRED

    # Configure HTTPClient to use SSL for Proxy Requests
    ssl_context = make_ssl_context(keyfile, certfile, client_ca)
    httpclient.AsyncHTTPClient.configure(None, defaults={"ssl_options": ssl_context})

    return ssl_options


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
        base_url=prefix,
        # Required for JupyterHub
        hub_user=os.environ.get("JUPYTERHUB_USER", ""),
        hub_group=os.environ.get("JUPYTERHUB_GROUP", ""),
        cookie_secret=os.urandom(32),
    )

    if websocket_max_message_size:
        app_log.debug(f"Restricting WebSocket Messages to {websocket_max_message_size}")
        settings["websocket_max_message_size"] = websocket_max_message_size

    escaped_prefix = re.escape(prefix)
    app = Application(
        [
            # Redirects from the JupyterHub might not contain a slash
            (f"^{escaped_prefix}$", RedirectHandler, dict(url=f"{escaped_prefix}/")),
            (f"^{escaped_prefix}/oauth_callback", HubOAuthCallbackHandler),
            (
                f"^{escaped_prefix}/(.*)",
                Proxy,
                dict(
                    state={},
                    # ToDo: progressive=progressive
                ),
            ),
        ],
        **settings,
    )

    return app
