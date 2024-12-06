from __future__ import annotations

import logging
import os
import re
import ssl
from textwrap import dedent
from urllib.parse import urlparse

from jupyterhub.services.auth import HubOAuthCallbackHandler
from jupyterhub.utils import make_ssl_context
from tornado import httpclient, httpserver, ioloop, web
from tornado.web import RedirectHandler
from traitlets.config import Application as TraitletsApplication
from traitlets.traitlets import Bool, Int, Unicode, default, validate

from ..config import ServerProcess
from .activity import start_activity_update
from .proxy import make_proxy


class StandaloneProxyServer(TraitletsApplication, ServerProcess):
    name = "jupyter-standalone-proxy"
    description = """
    Wrap an arbitrary web service so it can be used in place of 'jupyterhub-singleuser' 
    in a JupyterHub setting. 
    
    Usage: jupyter standaloneproxy [options] -- <command>
    
    The <command> will be executed to start the web service once the proxy receives the first request. The command can
    contain the placeholders '{{port}}', '{{unix_socket}}' and '{{base_url}}', which will be replaced with the 
    appropriate values once the application starts.
    
    For more details, see the jupyter-server-proxy documentation.  
    """

    base_url = Unicode(
        help="""
        Base URL where Requests will be received and proxied. Usually taken from the 
        "JUPYTERHUB_SERVICE_PREFIX" environment variable (or "/" when not set). 
        Set to overwrite.

        When setting to "/foo/bar", only incoming requests starting with this prefix will
        be answered by the server and proxied to the proxied app. Any other requests will
        get a 404 response.
        """,
    ).tag(config=True)

    @default("prefix")
    def _default_prefix(self):
        return os.environ.get("JUPYTERHUB_SERVICE_PREFIX", "/").removesuffix("/")

    @validate("prefix")
    def _validate_prefix(self, proposal):
        return proposal["value"].removesuffix("/")

    skip_authentication = Bool(
        default=False,
        help="""
        Do not authenticate access to the server via JupyterHub. When set,
        incoming requests will not be authenticated and anyone can access the
        application.

        WARNING: Disabling Authentication can be a major security issue.
        """,
    ).tag(config=True)

    address = Unicode(
        help="""
        The address where the proxy server can be accessed. The address is usually taken from the `JUPYTERHUB_SERVICE_URL`
        environment variable or will default to `127.0.0.1`. Used to explicitely overwrite the address of the server.
        """
    ).tag(config=True)

    @default("address")
    def _default_address(self):
        if os.environ.get("JUPYTERHUB_SERVICE_URL"):
            url = urlparse(os.environ["JUPYTERHUB_SERVICE_URL"])
            if url.hostname:
                return url.hostname

        return "127.0.0.1"

    port = Int(
        help="""
        The port where the proxy server can be accessed. The port is usually taken from the `JUPYTERHUB_SERVICE_URL`
        environment variable or will default to `8888`. Used to explicitely overwrite the port of the server.
        """
    ).tag(config=True)

    @default("port")
    def _default_port(self):
        if os.environ.get("JUPYTERHUB_SERVICE_URL"):
            url = urlparse(os.environ["JUPYTERHUB_SERVICE_URL"])

            if url.port:
                return url.port
            elif url.scheme == "http":
                return 80
            elif url.scheme == "https":
                return 443

        return 8888

    server_port = Int(default_value=0, help=ServerProcess.port.help).tag(config=True)

    activity_interval = Int(
        default_value=300,
        help="""
        Specify an interval to send regulat activity updated to the JupyterHub (in Seconds). 
        When enabled, the StandaloneProxy will try to send a POST request to the JupyterHub API
        containing a timestamp and the name of the server.
        The URL for the activity Endpoint needs to be specified in the "JUPYTERHUB_ACTIVITY_URL"
        environment variable. This URL usually is "/api/users/<user>/activity".

        Set to 0 to disable activity notifications.
        """,
    ).tag(config=True)

    websocket_max_message_size = Int(
        default_value=None,
        allow_none=True,
        help="Restrict the size of a message in a WebSocket connection (in bytes). Tornado defaults to 10MiB.",
    ).tag(config=True)

    @default("command")
    def _default_command(self):
        # ToDo: Find a better way to do this
        return self.extra_args

    def __init__(self):
        super().__init__()

        # Flags for CLI
        self.flags = {
            **super().flags,
            "absolute-url": (
                {"ServerProcess": {"absolute_url": True}},
                dedent(ServerProcess.absolute_url.help),
            ),
            "raw-socket-proxy": (
                {"ServerProcess": {"raw_socket_proxy": True}},
                dedent(ServerProcess.raw_socket_proxy.help),
            ),
            "skip-authentication": (
                {"StandaloneProxyServer": {"skip_authentication": True}},
                dedent(self.__class__.skip_authentication.help),
            ),
        }

        # Create an Alias to all Traits defined in ServerProcess, with some
        # exeptions we do not need, for easier use of the CLI
        # We don't need "command" here, as we will take it from the extra_args
        ignore_traits = [
            "launcher_entry",
            "new_browser_tab",
            "rewrite_response",
            "update_last_activity",
            "command",
        ]
        server_process_aliases = {
            trait: f"ServerProcess.{trait}"
            for trait in ServerProcess.class_traits(config=True)
            if trait not in ignore_traits and trait not in self.flags
        }

        self.aliases = {
            **server_process_aliases,
            "base_url": "StandaloneProxyServer.base_url",
            "address": "StandaloneProxyServer.address",
            "port": "StandaloneProxyServer.port",
            "server_port": "StandaloneProxyServer.server_port",
            "activity_interval": "StandaloneProxyServer.activity_interval",
            "websocket_max_message_size": "StandaloneProxyServer.websocket_max_message_size",
        }

    def _create_app(self) -> web.Application:
        self.log.debug(f"Process will use port = {self.port}")
        self.log.debug(f"Process will use unix_socket = {self.unix_socket}")
        self.log.debug(f"Process environment: {self.environment}")
        self.log.debug(f"Proxy mappath: {self.mappath}")

        settings = dict(
            debug=self.log_level == logging.DEBUG,
            base_url=self.base_url,
            # Required for JupyterHub
            hub_user=os.environ.get("JUPYTERHUB_USER", ""),
            hub_group=os.environ.get("JUPYTERHUB_GROUP", ""),
            cookie_secret=os.urandom(32),
        )

        if self.websocket_max_message_size:
            self.log.debug(
                f"Restricting WebSocket Messages to {self.websocket_max_message_size}"
            )
            settings["websocket_max_message_size"] = self.websocket_max_message_size

        # Create the proxy class with out arguments
        proxy_handler, proxy_kwargs = make_proxy(
            self.command,
            self.server_port,
            self.unix_socket,
            self.environment,
            self.mappath,
            self.timeout,
            self.skip_authentication,
        )

        base_url = re.escape(self.base_url)
        return web.Application(
            [
                # Redirects from the JupyterHub might not contain a slash, so we add one here
                (f"^{base_url}$", RedirectHandler, dict(url=f"{base_url}/")),
                (f"^{base_url}/oauth_callback", HubOAuthCallbackHandler),
                (f"^{base_url}/(.*)", proxy_handler, proxy_kwargs),
            ],
            **settings,
        )

    def _configure_ssl(self) -> dict | None:
        # See https://github.com/jupyter-server/jupyter_server/blob/v2.0.0/jupyter_server/serverapp.py#L2053-L2073
        keyfile = os.environ.get("JUPYTERHUB_SSL_KEYFILE", "")
        certfile = os.environ.get("JUPYTERHUB_SSL_CERTFILE", "")
        client_ca = os.environ.get("JUPYTERHUB_SSL_CLIENT_CA", "")

        if not (keyfile or certfile or client_ca):
            self.log.warn("Could not configure SSL")
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
        httpclient.AsyncHTTPClient.configure(
            None, defaults={"ssl_options": ssl_context}
        )

        return ssl_options

    def start(self):
        if self.skip_authentication:
            self.log.warn("Disabling Authentication with JuypterHub Server!")

        app = self._create_app()

        ssl_options = self._configure_ssl()
        http_server = httpserver.HTTPServer(app, ssl_options=ssl_options, xheaders=True)
        http_server.listen(self.port, self.address)

        self.log.info(f"Starting standaloneproxy on '{self.address}:{self.port}'")
        self.log.info(f"Base URL: {self.base_url!r}")
        self.log.info(f"Command: {' '.join(self.command)!r}")

        # Periodically send JupyterHub Notifications, that we are still running
        if self.activity_interval > 0:
            self.log.info(
                f"Sending Acitivity Notivication to JupyterHub with interval={self.activity_interval}s"
            )
            start_activity_update(self.activity_interval)

        ioloop.IOLoop.current().start()
