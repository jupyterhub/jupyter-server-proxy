import sys
from pathlib import Path


def _get_path(*args):
    """Resolve a path relative to this file"""
    return str(Path(__file__).parent.resolve().joinpath(*args))


sys.path.append(_get_path())

# load the config object for traitlets based configuration
c = get_config()  # noqa


def mappathf(path):
    p = path + "mapped"
    return p


def translate_ciao(path, host, response, orig_response, port):
    # Assume that the body has not been modified by any previous rewrite
    assert response.body == orig_response.body

    response.code = 418
    response.reason = "I'm a teapot"
    response.headers["i-like"] = "tacos"
    response.headers["Proxied-Host-Port"] = f"{host}:{port}"
    response.headers["Proxied-Path"] = path
    response.body = response.body.replace(b"ciao", b"hello")


def hello_to_foo(response):
    response.body = response.body.replace(b"hello", b"foo")


# Example from the rewrite_response docstring
def dog_to_cat(response):
    response.headers["I-Like"] = "tacos"
    response.body = response.body.replace(b"dog", b"cat")


# Example from the rewrite_response docstring
def cats_only(response, path):
    if path.startswith("/cat-club"):
        response.code = 403
        response.body = b"dogs not allowed"


def my_env():
    return {"MYVAR": "String with escaped {{var}}"}


c.ServerProxy.servers = {
    "python-http": {
        "command": [sys.executable, _get_path("httpinfo.py"), "--port={port}"],
    },
    "python-http-abs": {
        "command": [sys.executable, _get_path("httpinfo.py"), "--port={port}"],
        "absolute_url": True,
    },
    "python-http-port54321": {
        "command": [sys.executable, _get_path("httpinfo.py"), "--port={port}"],
        "port": 54321,
    },
    "python-http-mappath": {
        "command": [sys.executable, _get_path("httpinfo.py"), "--port={port}"],
        "mappath": {
            "/": "/index.html",
        },
    },
    "python-http-mappathf": {
        "command": [sys.executable, _get_path("httpinfo.py"), "--port={port}"],
        "mappath": mappathf,
    },
    "python-http-callable-env": {
        "command": [sys.executable, _get_path("httpinfo.py"), "--port={port}"],
        "environment": my_env,
    },
    "python-websocket": {
        "command": [sys.executable, _get_path("websocket.py"), "--port={port}"],
        "request_headers_override": {
            "X-Custom-Header": "pytest-23456",
        },
    },
    "python-eventstream": {
        "command": [sys.executable, _get_path("eventstream.py"), "--port={port}"]
    },
    "python-unix-socket-true": {
        "command": [
            sys.executable,
            _get_path("httpinfo.py"),
            "--unix-socket={unix_socket}",
        ],
        "unix_socket": True,
    },
    "python-unix-socket-file": {
        "command": [
            sys.executable,
            _get_path("httpinfo.py"),
            "--unix-socket={unix_socket}",
        ],
        "unix_socket": "/tmp/jupyter-server-proxy-test-socket",
    },
    "python-unix-socket-file-no-command": {
        # this server process can be started earlier by first interacting with
        # python-unix-socket-file
        "unix_socket": "/tmp/jupyter-server-proxy-test-socket",
    },
    "python-request-headers": {
        "command": [sys.executable, _get_path("httpinfo.py"), "--port={port}"],
        "request_headers_override": {
            "X-Custom-Header": "pytest-23456",
        },
    },
    "python-gzipserver": {
        "command": [sys.executable, _get_path("gzipserver.py"), "{port}"],
    },
    "python-http-rewrite-response": {
        "command": [sys.executable, _get_path("httpinfo.py"), "--port={port}"],
        "rewrite_response": translate_ciao,
        "port": 54323,
    },
    "python-chained-rewrite-response": {
        "command": [sys.executable, _get_path("httpinfo.py"), "--port={port}"],
        "rewrite_response": [translate_ciao, hello_to_foo],
    },
    "python-cats-only-rewrite-response": {
        "command": [sys.executable, _get_path("httpinfo.py"), "--port={port}"],
        "rewrite_response": [dog_to_cat, cats_only],
    },
    "python-dogs-only-rewrite-response": {
        "command": [sys.executable, _get_path("httpinfo.py"), "--port={port}"],
        "rewrite_response": [cats_only, dog_to_cat],
    },
    "python-proxyto54321-no-command": {"port": 54321},
    "python-rawsocket-tcp": {
        "command": [sys.executable, _get_path("rawsocket.py"), "{port}"],
        "raw_socket_proxy": True,
    },
    "python-rawsocket-unix": {
        "command": [sys.executable, _get_path("rawsocket.py"), "{unix_socket}"],
        "unix_socket": True,
        "raw_socket_proxy": True,
    },
}

c.ServerProxy.non_service_rewrite_response = hello_to_foo

c.ServerApp.jpserver_extensions = {"proxyextension": True}

c.NotebookApp.nbserver_extensions = {"proxyextension": True}

# disable notebook 7 banner
c.ServerApp.show_banner = False

# disable slow/noisy discovery of language servers
c.LanguageServerManager.autodetect = False
