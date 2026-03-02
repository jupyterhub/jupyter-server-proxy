from __future__ import annotations

import logging
import os
import re
import ssl
from textwrap import dedent
from urllib.parse import urlparse

from jupyter_core.application import JupyterApp
from jupyterhub.services.auth import HubOAuthCallbackHandler
from jupyterhub.utils import make_ssl_context
from tornado import httpclient, httpserver, ioloop, web
from tornado.web import RedirectHandler
from traitlets.traitlets import Bool, Int, Unicode, default, validate

from ..config import ServerProcess
from .activity import start_activity_update
from .proxy import make_standalone_proxy


class StandaloneProxyServer(JupyterApp, ServerProcess):
    name = "jupyter-standalone-proxy"
    description = """
    Wrap an arbitrary web service so it can be used in place of 'jupyterhub-singleuser' 
    in a JupyterHub setting. 
    
    Usage: jupyter standaloneproxy [options] -- <command>
    
    For more details, see the jupyter-server-proxy documentation.  
    """
    examples = "jupyter standaloneproxy -- voila --port={port} --no-browser /path/to/notebook.ipynb"

    base_url = Unicode(
        help="""
        Base URL where Requests will be received and proxied. Usually taken from the 
        "JUPYTERHUB_SERVICE_PREFIX" environment variable (or "/" when not set). 
        Set to override.

        When setting to "/foo/bar", only incoming requests starting with this prefix will
        be answered by the server and proxied to the proxied app. Any other requests will
        get a 404 response.
        """,
    ).tag(config=True)

    @default("base_url")
    def _default_prefix(self):
        # Python 3.8 does not support removesuffix
        prefix = os.environ.get("JUPYTERHUB_SERVICE_PREFIX", "/")
        if prefix[-1] == "/":
            prefix = prefix[:-1]
        return prefix

    @validate("base_url")
    def _validate_prefix(self, proposal):
        prefix = proposal["value"]
        if prefix[-1] == "/":
            prefix = prefix[:-1]
        return prefix

    no_authentication = Bool(
        default=False,
        help="""
        Do not authenticate access to the server via JupyterHub. When set,
        incoming requests will not be authenticated and anyone can access the
        application.

        WARNING: Disabling Authentication can be a major security issue.
        """,
    ).tag(config=True)

    address = Unicode(help="""
        The address where the proxy server can be accessed. The address is usually taken from the `JUPYTERHUB_SERVICE_URL`
        environment variable or will default to `127.0.0.1`. Used to explicitly override the address of the server.
        """).tag(config=True)

    @default("address")
    def _default_address(self):
        if os.environ.get("JUPYTERHUB_SERVICE_URL"):
            url = urlparse(os.environ["JUPYTERHUB_SERVICE_URL"])
            if url.hostname:
                return url.hostname

        return "127.0.0.1"

    port = Int(help="""
        The port where the proxy server can be accessed. The port is usually taken from the `JUPYTERHUB_SERVICE_URL`
        environment variable or will default to `8888`. Used to explicitly override the port of the server.
        """).tag(config=True)

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
        Specify an interval to send regular activity updates to the JupyterHub (in seconds). 
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
            "no-authentication": (
                {"StandaloneProxyServer": {"no_authentication": True}},
                dedent(self.__class__.no_authentication.help),
            ),
        }
        self.flags.pop("y")

        # Some traits in ServerProcess are not defined to be configurable, but we need that for the standalone proxy
        for name, trait in ServerProcess.class_own_traits().items():
            trait.tag(config=True)

        # Create an Alias to all Traits defined in ServerProcess, with some
        # exceptions we do not need, for easier use of the CLI
        # We don't need "command" here, as we will take it from the extra_args
        ignore_traits = [
            "name",
            "launcher_entry",
            "new_browser_tab",
            "rewrite_response",
            "update_last_activity",
            "command",
        ]
        server_process_aliases = {
            trait.replace("_", "-"): f"StandaloneProxyServer.{trait}"
            for trait in ServerProcess.class_traits(config=True)
            if trait not in ignore_traits and trait not in self.flags
        }

        self.aliases = {
            **super().aliases,
            **server_process_aliases,
            "base-url": "StandaloneProxyServer.base_url",
            "address": "StandaloneProxyServer.address",
            "port": "StandaloneProxyServer.port",
            "server-port": "StandaloneProxyServer.server_port",
            "activity-interval": "StandaloneProxyServer.activity_interval",
            "websocket-max-message-size": "StandaloneProxyServer.websocket_max_message_size",
        }

    def emit_alias_help(self):
        yield from super().emit_alias_help()
        yield ""

        # Manually yield the help for command, which we will get from extra_args
        command_help = StandaloneProxyServer.class_get_trait_help(
            ServerProcess.command
        ).split("\n")
        yield command_help[0].replace("--StandaloneProxyServer.command", "command")
        yield from command_help[1:]

    def get_proxy_base_class(self) -> tuple[type | None, dict]:
        cls, kwargs = super().get_proxy_base_class()
        if cls is None:
            return None, kwargs

        return make_standalone_proxy(cls, kwargs)

    def get_proxy_attributes(self) -> dict:
        attributes = super().get_proxy_attributes()

        # The ProxyHandler will be listening on "{base_url}/" instead of "{base_url}/{name}".
        # Needed for correct header generation of "X-Forwarded-Context", etc.
        attributes["proxy_base"] = "/"

        attributes["requested_port"] = self.server_port
        attributes["no_authentication"] = self.no_authentication

        return attributes

    def create_app(self) -> web.Application:
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

        # Create the proxy class without arguments
        proxy_handler, proxy_kwargs = self.make_proxy_handler()

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
        if self.no_authentication:
            self.log.warn("Disabling Authentication with JuypterHub Server!")

        app = self.create_app()

        ssl_options = self._configure_ssl()
        http_server = httpserver.HTTPServer(app, ssl_options=ssl_options, xheaders=True)
        http_server.listen(self.port, self.address)

        self.log.info(f"Starting standaloneproxy on '{self.address}:{self.port}'")
        self.log.info(f"Base URL: {self.base_url!r}")
        self.log.info(f"Command: {self.command}")

        # Periodically send JupyterHub Notifications, that we are still running
        if self.activity_interval > 0:
            self.log.info(
                f"Sending Activity Notification to JupyterHub with interval={self.activity_interval}s"
            )
            start_activity_update(self.activity_interval)

        ioloop.IOLoop.current().start()
