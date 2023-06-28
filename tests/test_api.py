"""Tests for API endpoints"""

import json
import os
import time
from http.client import HTTPConnection
from typing import Tuple

import pytest
from traitlets.config.loader import PyFileConfigLoader

# use ipv4 for CI, etc.
LOCALHOST = "127.0.0.1"


def request_get(port, path, token, host=LOCALHOST):
    h = HTTPConnection(host, port, 10)
    if "?" in path:
        url = f"{path}&token={token}"
    else:
        url = f"{path}?token={token}"
    h.request("GET", url)
    return h.getresponse()


def request_delete(port, path, token, host=LOCALHOST):
    h = HTTPConnection(host, port, 10)
    if "?" in path:
        url = f"{path}&token={token}"
    else:
        url = f"{path}?token={token}"
    h.request("DELETE", url)
    return h.getresponse()


def load_config():
    """Load config file"""
    config_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        "jupyter_server_config.py",
    )
    cl = PyFileConfigLoader(config_file_path)
    return cl.load_config()


def start_proxies(PORT, TOKEN):
    """Start proxy servers for testing API handlers"""
    selected_servers = ["python-http", "python-unix-socket-true", "python-websocket"]
    for url in selected_servers:
        _ = request_get(PORT, f"/{url}/", TOKEN)
    return selected_servers


def test_server_proxy_info(a_server_port_and_token: Tuple[int, str]) -> None:
    """Test API endpoint of /server-proxy/api/servers-info."""
    PORT, TOKEN = a_server_port_and_token
    config = load_config()
    test_url = "/server-proxy/api/servers-info"
    expected_servers = list(config["ServerProxy"]["servers"].keys())
    r = request_get(PORT, test_url, TOKEN)
    data = json.loads(r.read().decode())
    found_servers = [sp["name"] for sp in data["server_processes"]]
    assert r.code == 200
    assert found_servers == expected_servers


def test_get_all_server_proxy(a_server_port_and_token: Tuple[int, str]) -> None:
    """Test API endpoint of /server-proxy/api/servers."""
    PORT, TOKEN = a_server_port_and_token
    expected_servers = start_proxies(PORT, TOKEN)
    test_url = "/server-proxy/api/servers/"
    r = request_get(PORT, test_url, TOKEN)
    data = json.loads(r.read().decode())
    found_servers = [sp["name"] for sp in data]
    assert r.code == 200
    assert found_servers == expected_servers


@pytest.mark.parametrize(
    "server_process_path",
    [
        "python-http",
        "python-unix-socket-true",
        "python-websocket",
    ],
)
def test_get_given_server_proxy(
    server_process_path: str, a_server_port_and_token: Tuple[int, str]
) -> None:
    """Test API GET endpoint of /server-proxy/api/servers/{name}."""
    PORT, TOKEN = a_server_port_and_token
    # config = load_config()
    # expected_data = config['ServerProxy']['servers'][server_process_path]
    _ = request_get(PORT, f"/{server_process_path}/", TOKEN)
    test_url = f"/server-proxy/api/servers/{server_process_path}"
    r = request_get(PORT, test_url, TOKEN)
    data = json.loads(r.read().decode())
    assert r.code == 200
    assert data["name"] == server_process_path
    if server_process_path in ["python-http", "python-websocket"]:
        assert isinstance(int(data["port"]), int)
        assert data["managed"] == True
        assert data["unix_socket"] == ""
    elif server_process_path == "python-unix-socket-true":
        assert int(data["port"]) == 0
        assert "jupyter-server-proxy" in data["unix_socket"]
        assert data["managed"] == True


def test_get_nonexisting_server_proxy(a_server_port_and_token: Tuple[int, str]) -> None:
    """Test API non existing GET endpoint of /server-proxy/api/servers/{name}."""
    PORT, TOKEN = a_server_port_and_token
    test_url = "/server-proxy/api/servers/doesnotexist"
    r = request_get(PORT, test_url, TOKEN)
    assert r.code == 404


@pytest.mark.parametrize(
    "server_process_path",
    [
        "python-http",
        "python-unix-socket-true",
        "python-websocket",
    ],
)
def test_delete_given_server_proxy(
    server_process_path: str, a_server_port_and_token: Tuple[int, str]
) -> None:
    """Test API DELETE endpoint of /server-proxy/api/servers/{name}."""
    PORT, TOKEN = a_server_port_and_token
    _ = request_get(PORT, f"/{server_process_path}/", TOKEN)
    # Just give enough time for it to be added in manager if it does not exist already
    time.sleep(1)
    test_url = f"/server-proxy/api/servers/{server_process_path}"
    r = request_delete(PORT, test_url, TOKEN)
    assert r.code == 204


def test_delete_nonexisting_server_proxy(
    a_server_port_and_token: Tuple[int, str]
) -> None:
    """Test API DELETE non existing endpoint of /server-proxy/api/servers/{name}."""
    PORT, TOKEN = a_server_port_and_token
    test_url = "/server-proxy/api/servers/doesnotexist"
    r = request_delete(PORT, test_url, TOKEN)
    assert r.code == 404
    # When no server name is supplied
    test_url = "/server-proxy/api/servers/"
    r = request_delete(PORT, test_url, TOKEN)
    assert r.code == 403
