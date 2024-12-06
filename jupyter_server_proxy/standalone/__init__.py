import argparse
import logging
import os
from urllib.parse import urlparse

from tornado import ioloop
from tornado.httpserver import HTTPServer
from tornado.log import app_log as log
from tornado.log import enable_pretty_logging, gen_log

from .activity import start_activity_update
from .proxy import configure_ssl, make_proxy_app


def _default_address_and_port() -> tuple[str, int]:
    """
    Get the Address and Port for the Proxy, either from JUPYTERHUB_SERVICE_URL or default values.
    See https://github.com/jupyterhub/jupyterhub/blob/4.x/jupyterhub/singleuser/mixins.py#L266-L284.
    """
    address = "127.0.0.1"
    port = 8888

    if os.environ.get("JUPYTERHUB_SERVICE_URL"):
        url = urlparse(os.environ["JUPYTERHUB_SERVICE_URL"])

        if url.hostname:
            address = url.hostname

        if url.port:
            port = url.port
        elif url.scheme == "http":
            port = 80
        elif url.scheme == "https":
            port = 443

    return address, port


def run(
    command: list[str],
    port: int | None,
    address: str | None,
    server_port: int,
    socket_path: str | None,
    socket_auto: bool,
    environment: list[tuple[str, str]] | None,
    mappath: list[tuple[str, str]] | None,
    debug: bool,
    # logs: bool,
    skip_authentication: bool,
    timeout: int,
    activity_interval: int,
    # progressive: bool,
    websocket_max_message_size: int,
):
    # Setup Logging
    enable_pretty_logging(logger=log)
    if debug:
        log.setLevel(logging.DEBUG)
        gen_log.setLevel(logging.DEBUG)

    address_port_default = _default_address_and_port()
    address = address or address_port_default[0]
    port = port or address_port_default[1]

    if skip_authentication:
        log.warn("Disabling Authentication with JuypterHub Server!")

    prefix = os.environ.get("JUPYTERHUB_SERVICE_PREFIX", "/")

    app = make_proxy_app(
        command,
        prefix.removesuffix("/"),
        server_port,
        socket_path or socket_auto,
        dict(environment),
        dict(mappath),
        timeout,
        skip_authentication,
        debug,
        # progressive,
        websocket_max_message_size,
    )

    ssl_options = configure_ssl()
    http_server = HTTPServer(app, ssl_options=ssl_options, xheaders=True)
    http_server.listen(port, address)

    log.info(f"Starting standaloneproxy on '{address}:{port}'")
    log.info(f"URL Prefix: {prefix!r}")
    log.info(f"Command: {' '.join(command)!r}")

    # Periodically send JupyterHub Notifications, that we are still running
    if activity_interval > 0:
        log.info(
            f"Sending Acitivity Notivication to JupyterHub with interval={activity_interval}s"
        )
        start_activity_update(activity_interval)

    ioloop.IOLoop.current().start()


def main():
    parser = argparse.ArgumentParser(
        "jupyter-standalone-proxy",
        description="Wrap an arbitrary WebApp so it can be used in place of 'jupyterhub-singleuser' in a JupyterHub setting.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-p",
        "--port",
        type=int,
        dest="port",
        help="Set port for the proxy server to listen on. Will use 'JUPYTERHUB_SERVICE_URL' or '127.0.0.1' by default.",
    )
    parser.add_argument(
        "-a",
        "--address",
        type=str,
        dest="address",
        help="Set address for the proxy server to listen on. Will use 'JUPYTERHUB_SERVICE_URL' or '8888' by default.",
    )
    parser.add_argument(
        "-s",
        "--server-port",
        default=0,
        type=int,
        dest="server_port",
        help="Port for the WebApp should end up running on (0 for random open port).",
    )
    parser.add_argument(
        "--socket-path",
        type=str,
        default=None,
        help="Path to the Unix Socket to use for proxying. Takes precedence over '-s/--server_port' and '--socket-auto'.",
    )
    parser.add_argument(
        "--socket-auto",
        action="store_true",
        help="Use Unix Socket for proxying, but let Jupyter Server Proxy automatically create one.",
    )
    parser.add_argument(
        "--env",
        "--environment",
        type=lambda v: tuple(v.split(":")[:2]),
        default=[],
        action="append",
        dest="environment",
        help="Add an environment variable to the server process. Must be of the form <Name>:<Value>, e.g. --env=MY_VAR:42",
    )
    parser.add_argument(
        "--mappath",
        type=lambda v: tuple(v.split(":")[:2]),
        default=[],
        action="append",
        help="Add an path mapping to the proxy. Any requests received under <Source> will be redirected to <Target>. "
        "Must be of the form <Source>:<Target>, e.g. --mappath=/:/index.html",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        default=False,
        dest="debug",
        help="Display debug level logs.",
    )
    # ToDo: Split Server and Application Logger
    # parser.add_argument(
    #     "--logs",
    #     action="store_true",
    #     default=True,
    #     help="Display logs generated by the subprocess.",
    # )
    parser.add_argument(
        "--skip-authentication",
        action="store_true",
        help="Do not enforce authentication with the JupyterHub Server.",
    )
    parser.add_argument(
        "--timeout",
        default=60,
        type=int,
        help="Timeout to wait until the subprocess has started and can be addressed.",
    )
    parser.add_argument(
        "--activity-interval",
        default=300,
        type=int,
        help="Frequency to notify Hub that the WebApp is still running (In seconds, 0 for never).",
    )
    # ToDo: Progressive Proxy
    # parser.add_argument(
    #     "--progressive",
    #     action="store_true",
    #     default=False,
    #     help="Progressively flush responses as they arrive (good for Voila).",
    # )
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
