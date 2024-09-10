import argparse
import json
import logging
import os
import re
from datetime import datetime
from urllib.parse import urlparse

from jupyterhub import __version__ as __jh_version__
from jupyterhub.services.auth import HubOAuthCallbackHandler
from jupyterhub.utils import exponential_backoff, isoformat, make_ssl_context
from tornado import httpclient, ioloop
from tornado.httpserver import HTTPServer
from tornado.log import app_log
from tornado.web import Application, RedirectHandler, RequestHandler

from .handlers import SuperviseAndProxyHandler


def configure_http_client():
    keyfile = os.environ.get("JUPYTERHUB_SSL_KEYFILE", "")
    certfile = os.environ.get("JUPYTERHUB_SSL_CERTFILE", "")
    client_ca = os.environ.get("JUPYTERHUB_SSL_CLIENT_CA", "")

    if keyfile == "" and certfile == "" and client_ca == "":
        return

    ssl_context = make_ssl_context(keyfile, certfile, cafile=client_ca)
    httpclient.AsyncHTTPClient.configure(None, defaults={"ssl_options": ssl_context})


def _make_native_proxy_handler(command, environment, port, mappath):
    """
    Create a SuperviseAndProxyHandler subclass with given parameters
    """

    class _Proxy(SuperviseAndProxyHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.proxy_base = command[0]
            self.requested_port = port
            self.mappath = mappath
            self.command = command

            # ToDo?
            self.origin_host = None

        # ToDo!
        def prepare(self, *args, **kwargs):
            pass

        # ToDo!
        def skip_check_origin(self) -> bool:
            return True

        @property
        def process_args(self):
            return {
                "port": self.port,
                "base_url": self.base_url,
                # "presentation_path": self.presentation_path,
                # "presentation_basename": self.presentation_basename,
                # "presentation_dirname": self.presentation_dirname,
                "origin_host": self.request.host,  # ToDo!
                "-": "-",
                "--": "--",
            }

        @property
        def base_url(self):
            return self.settings.get("base_url", "/")

        # @property
        # def presentation_path(self):
        #     return self.settings.get("presentation_path", ".")
        #
        # @property
        # def presentation_basename(self):
        #     return self.settings.get("presentation_basename", "")
        #
        # @property
        # def presentation_dirname(self):
        #     return self.settings.get("presentation_dirname", ".")

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

        def _render_template(self, value):
            args = self.process_args
            if type(value) is str:
                return value.format(**args)
            elif type(value) is list:
                return [self._render_template(v) for v in value]
            elif type(value) is dict:
                return {
                    self._render_template(k): self._render_template(v)
                    for k, v in value.items()
                }
            else:
                raise ValueError(f"Value of unrecognized type {type(value)}")

        def get_env(self):
            if callable(environment):
                raise Exception(
                    "return self._render_template(call_with_asked_args(environment, self.process_args))"
                )
            else:
                return self._render_template(environment)

        def get_timeout(self):
            return 60

    return _Proxy


def patch_default_headers():
    if hasattr(RequestHandler, "_orig_set_default_headers"):
        return
    RequestHandler._orig_set_default_headers = RequestHandler.set_default_headers

    def set_jupyterhub_header(self):
        self._orig_set_default_headers()
        self.set_header("X-JupyterHub-Version", __jh_version__)

    RequestHandler.set_default_headers = set_jupyterhub_header


def make_app(
    destport,
    prefix,
    command,
    authtype,
    request_timeout,
    debug,
    logs,
    forward_user_info,
    query_user_info,
    progressive,
    websocket_max_message_size,
):
    # ToDo: Presentation_path?
    # presentation_basename = ""
    # presentation_dirname = ""
    #
    # if presentation_path:
    #     if not os.path.isabs(presentation_path):
    #         presentation_path = os.path.join(os.getcwd(), presentation_path)
    #     presentation_basename = os.path.basename(presentation_path)
    #     presentation_dirname = os.path.dirname(presentation_path)

    patch_default_headers()

    proxy_handler = _make_native_proxy_handler(command, {}, destport, {})

    options = dict(
        debug=debug,
        logs=logs,
        cookie_secret=os.urandom(32),
        user=os.environ.get("JUPYTERHUB_USER") or "",
        group=os.environ.get("JUPYTERHUB_GROUP") or "",
        anyone=os.environ.get("JUPYTERHUB_ANYONE") or "",
        base_url=prefix,  # This is a confusing name, sorry
        # presentation_path=presentation_path,
        # presentation_basename=presentation_basename,
        # presentation_dirname=presentation_dirname,
        request_timeout=request_timeout,
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
                    # ToDo: authtype=authtype, forward_user_info=forward_user_info, query_user_info=query_user_info, progressive=progressive
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


def start_keep_alive(last_activity_interval, force_alive, settings):
    client = httpclient.AsyncHTTPClient()

    hub_activity_url = os.environ.get("JUPYTERHUB_ACTIVITY_URL", "")
    server_name = os.environ.get("JUPYTERHUB_SERVER_NAME", "")
    api_token = os.environ.get("JUPYTERHUB_API_TOKEN", "")

    if api_token == "" or server_name == "" or hub_activity_url == "":
        print(
            "The following env vars are required to report activity back to the hub for keep alive: "
            "JUPYTERHUB_ACTIVITY_URL ({}), JUPYTERHUB_SERVER_NAME({})".format(
                hub_activity_url, server_name, api_token
            )
        )
        return

    async def send_activity():
        async def notify():
            print("About to notify Hub of activity")

            last_activity_timestamp = None

            if force_alive:
                last_activity_timestamp = datetime.utcnow()
            else:
                last_activity_timestamp = settings.get("api_last_activity", None)

            if last_activity_timestamp:
                last_activity_timestamp = isoformat(last_activity_timestamp)
                req = httpclient.HTTPRequest(
                    url=hub_activity_url,
                    method="POST",
                    headers={
                        "Authorization": f"token {api_token}",
                        "Content-Type": "application/json",
                    },
                    body=json.dumps(
                        {
                            "servers": {
                                server_name: {"last_activity": last_activity_timestamp}
                            },
                            "last_activity": last_activity_timestamp,
                        }
                    ),
                )
                try:
                    await client.fetch(req)
                except Exception as e:
                    print(f"Error notifying Hub of activity: {e}")
                    return False
                else:
                    return True

            return True  # Nothing to report, so really it worked

        await exponential_backoff(
            notify,
            fail_message="Failed to notify Hub of activity",
            start_wait=1,
            max_wait=15,
            timeout=60,
        )

    pc = ioloop.PeriodicCallback(send_activity, 1e3 * last_activity_interval, 0.1)
    pc.start()


def run(
    command: list[str],
    port=None,
    destport=0,
    ip="localhost",
    debug=False,
    logs=True,
    authtype="oauth",
    request_timeout=300,
    last_activity_interval=300,
    force_alive=True,
    forward_user_info=False,
    query_user_info=False,
    progressive=False,
    websocket_max_message_size=0,
):
    if port is None:
        get_port_from_env()

    if debug:
        app_log.setLevel(logging.DEBUG)
    elif logs:
        app_log.setLevel(logging.INFO)

    prefix = os.environ.get("JUPYTERHUB_SERVICE_PREFIX", "/")

    if len(prefix) > 0 and prefix[-1] == "/":
        prefix = prefix[:-1]

    configure_http_client()

    app = make_app(
        destport,
        prefix,
        list(command),
        authtype,
        request_timeout,
        debug,
        logs,
        forward_user_info,
        query_user_info,
        progressive,
        websocket_max_message_size,
    )

    ssl_options = get_ssl_options()

    http_server = HTTPServer(app, ssl_options=ssl_options, xheaders=True)

    http_server.listen(port or get_port_from_env(), ip)

    print(
        f"Starting jhsingle-native-proxy server on address {ip} port {port}, proxying to port {destport}"
    )
    print(f"URL Prefix: {prefix}")
    print(f"Auth Type: {authtype}")
    print(f"Command: {command}")

    if last_activity_interval > 0:
        start_keep_alive(last_activity_interval, force_alive, app.settings)

    ioloop.IOLoop.current().start()


def main():
    parser = argparse.ArgumentParser(
        "jupyter-native-proxy",
        description="Wrap an arbitrary WebApp so it can be used in place of 'singleuser' in a JupyterHub setting",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--port",
        default=None,
        type=int,
        help="Port for the proxy server to listen on. Defaults to JupyterHub default.",
    )
    parser.add_argument(
        "--destport",
        default=0,
        type=int,
        help="Port for the WebApp should end up running on. Leave at 0 for a random open port.",
    )
    parser.add_argument("--ip", default="localhost", help="Address to listen on.")
    parser.add_argument(
        "--debug", action="store_true", default=False, help="Display debug level logs."
    )
    parser.add_argument(
        "--logs",
        action="store_true",
        default=True,
        help="Display logs generated by the subprocess.",
    )
    parser.add_argument(
        "--authtype",
        choices=["oauth", "none"],
        default="oauth",
        help="Authentication Metod.",
    )
    parser.add_argument(
        "--request-timeout",
        default=300,
        type=int,
        help="Timeout for proxied HTTP calls to subprocess in seconds.",
    )
    parser.add_argument(
        "--last-activity-interval",
        default=300,
        type=int,
        help="Frequency to notify Hub that the WebApp is still running in seconds. 0 for never.",
    )
    parser.add_argument(
        "--force-alive",
        action="store_true",
        default=True,
        help="Always report, that there has been activity (force keep alive) - only if last-activity-interval > 0.",
    )
    parser.add_argument(
        "--forward-user-info",
        action="store_true",
        default=False,
        help="Forward a 'X-CDSDASHBOARDS-JH-USER' HTTP header to process containing JupyterHub user data.",
    )
    parser.add_argument(
        "--query-user-info",
        action="store_true",
        default=False,
        help="Add a 'CDSDASHBOARDS_JH_USER GET' query arg in HTTP request to process containing JupyterHub user data.",
    )
    parser.add_argument(
        "--progressive",
        action="store_true",
        default=False,
        help="Progressively flush responses as they arrive (good for Voila).",
    )
    parser.add_argument(
        "--websocket-max-message-size",
        default=0,
        type=int,
        help="Max size of websocket data (leave at 0 for library defaults).",
    )
    parser.add_argument(
        "command", nargs="+", help="The command executed for starting the WebApp"
    )

    args = parser.parse_args()
    run(**vars(args))


if __name__ == "__main__":
    main()
