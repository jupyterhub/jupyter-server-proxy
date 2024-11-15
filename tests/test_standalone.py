import sys
from pathlib import Path

import pytest
from tornado import testing

from jupyter_server_proxy.standalone import _default_address_and_port, make_proxy_app

"""
Test if address and port are identified correctly
"""


def test_address_and_port_with_http_address(monkeypatch):
    monkeypatch.setenv("JUPYTERHUB_SERVICE_URL", "http://localhost/")
    address, port = _default_address_and_port()

    assert address == "localhost"
    assert port == 80


def test_address_and_port_with_https_address(monkeypatch):
    monkeypatch.setenv("JUPYTERHUB_SERVICE_URL", "https://localhost/")
    address, port = _default_address_and_port()

    assert address == "localhost"
    assert port == 443


def test_address_and_port_with_address_and_port(monkeypatch):
    monkeypatch.setenv("JUPYTERHUB_SERVICE_URL", "http://localhost:7777/")
    address, port = _default_address_and_port()

    assert address == "localhost"
    assert port == 7777


def make_app(unix_socket: bool, skip_authentication: bool):
    command = [
        sys.executable,
        str(Path(__file__).parent / "resources" / "httpinfo.py"),
        "--port={port}",
        "--unix-socket={unix_socket}",
    ]

    return make_proxy_app(
        command=command,
        prefix="/some/prefix",
        port=0,
        unix_socket=unix_socket,
        environment={},
        mappath={},
        timeout=60,
        skip_authentication=skip_authentication,
        debug=True,
        websocket_max_message_size=0,
    )


class TestStandaloneProxyRedirect(testing.AsyncHTTPTestCase):
    """
    Ensure requests are proxied to the application. We need to disable authentication here,
    as we do not want to be redirected to the JupyterHub Login.
    """

    runTest = None  # Required for Tornado 6.1

    def get_app(self):
        return make_app(False, True)

    def test_add_slash(self):
        response = self.fetch("/some/prefix", follow_redirects=False)

        assert response.code == 301
        assert response.headers.get("Location") == "/some/prefix/"

    def test_without_prefix(self):
        response = self.fetch("/some/other/prefix")

        assert response.code == 404

    def test_on_prefix(self):
        response = self.fetch("/some/prefix/")
        assert response.code == 200

        body = response.body.decode()
        assert body.startswith("GET /")
        assert "X-Forwarded-Context: /some/prefix/" in body
        assert "X-Proxycontextpath: /some/prefix/" in body


@pytest.mark.skipif(
    sys.platform == "win32", reason="Unix socket not supported on Windows"
)
class TestStandaloneProxyWithUnixSocket(testing.AsyncHTTPTestCase):
    runTest = None  # Required for Tornado 6.1

    def get_app(self):
        return make_app(True, True)

    def test_with_unix_socket(self):
        response = self.fetch("/some/prefix/")
        assert response.code == 200

        body = response.body.decode()
        assert body.startswith("GET /")
        assert "X-Forwarded-Context: /some/prefix/" in body
        assert "X-Proxycontextpath: /some/prefix/" in body


class TestStandaloneProxyLogin(testing.AsyncHTTPTestCase):
    """
    Ensure we redirect to JupyterHub login when authentication is enabled
    """

    runTest = None  # Required for Tornado 6.1

    def get_app(self):
        return make_app(False, False)

    def test_redirect_to_login_url(self):
        response = self.fetch("/some/prefix/", follow_redirects=False)

        assert response.code == 302
        assert "Location" in response.headers
