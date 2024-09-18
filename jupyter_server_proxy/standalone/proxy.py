import os
import re
from urllib.parse import urlparse

from jupyterhub import __version__ as __jh_version__
from jupyterhub.services.auth import HubOAuthCallbackHandler, HubOAuthenticated
from jupyterhub.utils import make_ssl_context
from tornado import httpclient
from tornado.web import Application, RedirectHandler
from tornado.websocket import WebSocketHandler

from ..handlers import ProxyHandler, SuperviseAndProxyHandler


def configure_http_client():
    keyfile = os.environ.get("JUPYTERHUB_SSL_KEYFILE", "")
    certfile = os.environ.get("JUPYTERHUB_SSL_CERTFILE", "")
    client_ca = os.environ.get("JUPYTERHUB_SSL_CLIENT_CA", "")

    if keyfile == "" and certfile == "" and client_ca == "":
        return

    ssl_context = make_ssl_context(keyfile, certfile, cafile=client_ca)
    httpclient.AsyncHTTPClient.configure(None, defaults={"ssl_options": ssl_context})


class StandaloneProxyHandler(SuperviseAndProxyHandler):
    """
    Base class for standalone proxies. Will not ensure any authentication!
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.environment = {}
        self.timeout = 60

    def prepare(self, *args, **kwargs):
        pass

    def check_origin(self, origin: str = None):
        # Skip JupyterHandler.check_origin
        return WebSocketHandler.check_origin(self, origin)

    def get_env(self):
        return self._render_template(self.environment)

    def get_timeout(self):
        return self.timeout


class StandaloneHubProxyHandler(StandaloneProxyHandler, HubOAuthenticated):
    """
    Standalone Proxy used when spawned by a JupyterHub.
    Will restrict access to the application by authentication with the JupyterHub API.
    """

    @property
    def hub_users(self):
        return {self.settings["user"]}

    @property
    def hub_groups(self):
        if self.settings["group"]:
            return {self.settings["group"]}
        return set()

    @property
    def allow_all(self):
        if "anyone" in self.settings:
            return self.settings["anyone"] == "1"
        return super().allow_all

    def prepare(self, *args, **kwargs):
        # Enable Authentication Check
        return ProxyHandler.prepare(self, *args, **kwargs)

    def set_default_headers(self):
        self.set_header("X-JupyterHub-Version", __jh_version__)


def _make_native_proxy_handler(
    command, port, mappath, overwrite_authentication, environment, timeout
):
    """
    Create a StandaloneHubProxyHandler subclass with given parameters
    """

    # Try to determine if we are launched by a JupyterHub via environment variables.
    # See jupyterhub/spawner.py#L1035
    if overwrite_authentication is not None:
        base = (
            StandaloneHubProxyHandler
            if overwrite_authentication is True
            else StandaloneProxyHandler
        )
    elif "JUPYTERHUB_API_TOKEN" in os.environ and "JUPYTERHUB_API_URL" in os.environ:
        base = StandaloneHubProxyHandler
    else:
        base = StandaloneProxyHandler

    class _Proxy(base):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.name = command[0]
            self.proxy_base = command[0]
            self.requested_port = port
            self.mappath = mappath
            self.command = command
            self.environment = environment
            self.timeout = timeout

    return _Proxy


def make_app(
    destport,
    prefix,
    command,
    authtype,
    timeout,
    debug,
    logs,
    progressive,
    websocket_max_message_size,
):
    # ToDo: Environment
    proxy_handler = _make_native_proxy_handler(
        command, destport, {}, authtype, {}, timeout
    )

    options = dict(
        debug=debug,
        logs=logs,
        cookie_secret=os.urandom(32),
        user=os.environ.get("JUPYTERHUB_USER") or "",
        group=os.environ.get("JUPYTERHUB_GROUP") or "",
        anyone=os.environ.get("JUPYTERHUB_ANYONE") or "",
        base_url=prefix,  # This is a confusing name, sorry
    )

    if websocket_max_message_size:
        options["websocket_max_message_size"] = websocket_max_message_size

    return Application(
        [
            (
                r"^" + re.escape(prefix) + r"/oauth_callback",
                HubOAuthCallbackHandler,
            ),
            (
                r"^" + re.escape(prefix) + r"/(.*)",
                proxy_handler,
                dict(
                    state={},
                    # ToDo: progressive=progressive
                ),
            ),
            (
                r"^" + re.escape(prefix.replace("@", "%40")) + r"/(.*)",
                RedirectHandler,
                dict(url=prefix + "/{0}"),
            ),
        ],
        **options,
    )


def get_ssl_options():
    ssl_options = {}
    keyfile = os.environ.get("JUPYTERHUB_SSL_KEYFILE") or ""
    certfile = os.environ.get("JUPYTERHUB_SSL_CERTFILE") or ""
    client_ca = os.environ.get("JUPYTERHUB_SSL_CLIENT_CA") or ""

    if keyfile:
        ssl_options["keyfile"] = keyfile

    if certfile:
        ssl_options["certfile"] = certfile

    if client_ca:
        ssl_options["ca_certs"] = client_ca

    if not ssl_options:
        # None indicates no SSL config
        ssl_options = None
    else:
        # SSL may be missing, so only import it if it"s to be used
        import ssl

        # PROTOCOL_TLS selects the highest ssl/tls protocol version that both the client and
        # server support. When PROTOCOL_TLS is not available use PROTOCOL_SSLv23.
        # PROTOCOL_TLS is new in version 2.7.13, 3.5.3 and 3.6
        ssl_options.setdefault(
            "ssl_version", getattr(ssl, "PROTOCOL_TLS", ssl.PROTOCOL_SSLv23)
        )
        if ssl_options.get("ca_certs", False):
            ssl_options.setdefault("cert_reqs", ssl.CERT_REQUIRED)

    return ssl_options


# https://github.com/jupyterhub/jupyterhub/blob/2.0.0rc3/jupyterhub/singleuser/mixins.py#L340-L349
def get_port_from_env():
    if os.environ.get("JUPYTERHUB_SERVICE_URL"):
        url = urlparse(os.environ["JUPYTERHUB_SERVICE_URL"])
        if url.port:
            return url.port
        elif url.scheme == "http":
            return 80
        elif url.scheme == "https":
            return 443
    return 8888
