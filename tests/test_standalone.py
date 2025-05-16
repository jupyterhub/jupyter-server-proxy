import logging
import sys
from pathlib import Path

import pytest
from tornado import testing

from jupyter_server_proxy.standalone import StandaloneProxyServer

"""
Test if address and port are identified correctly
"""


def test_address_and_port_with_http_address(monkeypatch):
    monkeypatch.setenv("JUPYTERHUB_SERVICE_URL", "http://localhost/")
    proxy_server = StandaloneProxyServer()

    assert proxy_server.address == "localhost"
    assert proxy_server.port == 80


def test_address_and_port_with_https_address(monkeypatch):
    monkeypatch.setenv("JUPYTERHUB_SERVICE_URL", "https://localhost/")
    proxy_server = StandaloneProxyServer()

    assert proxy_server.address == "localhost"
    assert proxy_server.port == 443


def test_address_and_port_with_address_and_port(monkeypatch):
    monkeypatch.setenv("JUPYTERHUB_SERVICE_URL", "http://localhost:7777/")
    proxy_server = StandaloneProxyServer()

    assert proxy_server.address == "localhost"
    assert proxy_server.port == 7777


class _TestStandaloneBase(testing.AsyncHTTPTestCase):
    runTest = None  # Required for Tornado 6.1

    unix_socket: bool
    skip_authentication: bool

    def get_app(self):
        command = [
            sys.executable,
            str(Path(__file__).parent / "resources" / "httpinfo.py"),
            "--port={port}",
            "--unix-socket={unix_socket}",
        ]

        proxy_server = StandaloneProxyServer(
            command=command,
            base_url="/some/prefix",
            unix_socket=self.unix_socket,
            timeout=60,
            skip_authentication=self.skip_authentication,
            log_level=logging.DEBUG,
        )

        return proxy_server.create_app()


class TestStandaloneProxyRedirect(_TestStandaloneBase):
    """
    Ensure requests are proxied to the application. We need to disable authentication here,
    as we do not want to be redirected to the JupyterHub Login.
    """

    unix_socket = False
    skip_authentication = True

    def test_add_slash(self):
        response = self.fetch("/some/prefix", follow_redirects=False)

        assert response.code == 301
        assert response.headers.get("Location") == "/some/prefix/"

    def test_wrong_prefix(self):
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
class TestStandaloneProxyWithUnixSocket(_TestStandaloneBase):
    unix_socket = True
    skip_authentication = True

    def test_with_unix_socket(self):
        response = self.fetch("/some/prefix/")
        assert response.code == 200

        body = response.body.decode()
        assert body.startswith("GET /")
        assert "X-Forwarded-Context: /some/prefix/" in body
        assert "X-Proxycontextpath: /some/prefix/" in body


class TestStandaloneProxyLogin(_TestStandaloneBase):
    """
    Ensure we redirect to JupyterHub login when authentication is enabled
    """

    unix_socket = False
    skip_authentication = False

    def test_redirect_to_login_url(self):
        response = self.fetch("/some/prefix/", follow_redirects=False)

        assert response.code == 302
        assert "Location" in response.headers
