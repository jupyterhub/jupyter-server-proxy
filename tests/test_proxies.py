import asyncio
import json
import os
from http.client import HTTPConnection
from urllib.parse import quote
import pytest
from tornado.websocket import websocket_connect

PORT = os.getenv('TEST_PORT', 8888)
TOKEN = os.getenv('JUPYTER_TOKEN', 'secret')


def request_get(port, path, token, host='localhost'):
    h = HTTPConnection(host, port, 10)
    if '?' in path:
        url = '{}&token={}'.format(path, token)
    else:
        url = '{}?token={}'.format(path, token)
    h.request('GET', url)
    return h.getresponse()


def test_server_proxy_minimal_proxy_path_encoding():
    """Test that we don't encode anything more than we must to have a valid web
    request."""
    special_path = quote("Hello world 123 åäö 🎉你好世界±¥ :/[]@!$&'()*+,;=-._~", safe=":/?#[]@!$&'()*+,;=-._~")
    # NOTE: we left out ?# as they would interact badly with our requests_get
    # function's ability to pass the token query parameter.
    test_url = '/python-http/' + special_path
    r = request_get(PORT, test_url, TOKEN)
    assert r.code == 200
    s = r.read().decode('ascii')
    assert 'GET /{}?token='.format(special_path) in s

def test_server_proxy_minimal_proxy_path_encoding_complement():
    """Test that we don't encode ?# as a complement to the other test."""
    test_url = '/python-http/?token={}#test'.format(TOKEN)
    h = HTTPConnection('localhost', PORT, 10)
    r = request_get(PORT, test_url, TOKEN)
    h.request('GET', test_url)
    return h.getresponse()
    assert r.code == 200
    s = r.read().decode('ascii')
    assert 'GET /{}?token='.format(test_url) in s


def test_server_proxy_non_absolute():
    r = request_get(PORT, '/python-http/abc', TOKEN)
    assert r.code == 200
    s = r.read().decode('ascii')
    assert s.startswith('GET /abc?token=')
    assert 'X-Forwarded-Context: /python-http\n' in s
    assert 'X-Proxycontextpath: /python-http\n' in s


def test_server_proxy_absolute():
    r = request_get(PORT, '/python-http-abs/def', TOKEN)
    assert r.code == 200
    s = r.read().decode('ascii')
    assert s.startswith('GET /python-http-abs/def?token=')
    assert 'X-Forwarded-Context' not in s
    assert 'X-Proxycontextpath' not in s


def test_server_proxy_requested_port():
    r = request_get(PORT, '/python-http-port54321/ghi', TOKEN)
    assert r.code == 200
    s = r.read().decode('ascii')
    assert s.startswith('GET /ghi?token=')
    assert 'X-Forwarded-Context: /python-http-port54321\n' in s
    assert 'X-Proxycontextpath: /python-http-port54321\n' in s

    direct = request_get(54321, '/ghi', TOKEN)
    assert direct.code == 200


def test_server_proxy_port_non_absolute():
    r = request_get(PORT, '/proxy/54321/jkl', TOKEN)
    assert r.code == 200
    s = r.read().decode('ascii')
    assert s.startswith('GET /jkl?token=')
    assert 'X-Forwarded-Context: /proxy/54321\n' in s
    assert 'X-Proxycontextpath: /proxy/54321\n' in s


def test_server_proxy_port_absolute():
    r = request_get(PORT, '/proxy/absolute/54321/nmo', TOKEN)
    assert r.code == 200
    s = r.read().decode('ascii')
    assert s.startswith('GET /proxy/absolute/54321/nmo?token=')
    assert 'X-Forwarded-Context' not in s
    assert 'X-Proxycontextpath' not in s


@pytest.mark.parametrize(
    "requestpath,expected", [
        ('/', '/index.html?token='),
        ('/?q=1', '/index.html?q=1&token='),
        ('/pqr?q=2', '/pqr?q=2&token='),
    ]
)
def test_server_proxy_mappath_dict(requestpath, expected):
    r = request_get(PORT, '/python-http-mappath' + requestpath, TOKEN)
    assert r.code == 200
    s = r.read().decode('ascii')
    assert s.startswith('GET ' + expected)
    assert 'X-Forwarded-Context: /python-http-mappath\n' in s
    assert 'X-Proxycontextpath: /python-http-mappath\n' in s


@pytest.mark.parametrize(
    "requestpath,expected", [
        ('/', '/mapped?token='),
        ('/?q=1', '/mapped?q=1&token='),
        ('/stu?q=2', '/stumapped?q=2&token='),
    ]
)
def test_server_proxy_mappath_callable(requestpath, expected):
    r = request_get(PORT, '/python-http-mappathf' + requestpath, TOKEN)
    assert r.code == 200
    s = r.read().decode('ascii')
    assert s.startswith('GET ' + expected)
    assert 'X-Forwarded-Context: /python-http-mappathf\n' in s
    assert 'X-Proxycontextpath: /python-http-mappathf\n' in s


def test_server_proxy_remote():
    r = request_get(PORT, '/newproxy', TOKEN, host='127.0.0.1')
    assert r.code == 200


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


async def _websocket_echo():
    url = "ws://localhost:{}/python-websocket/echosocket".format(PORT)
    conn = await websocket_connect(url)
    expected_msg = "Hello, world!"
    await conn.write_message(expected_msg)
    msg = await conn.read_message()
    assert msg == expected_msg

def test_server_proxy_websocket(event_loop):
    event_loop.run_until_complete(_websocket_echo())


async def _websocket_subprotocols():
    url = "ws://localhost:{}/python-websocket/subprotocolsocket".format(PORT)
    conn = await websocket_connect(url, subprotocols=["protocol_1", "protocol_2"])
    await conn.write_message("Hello, world!")
    msg = await conn.read_message()
    assert json.loads(msg) == ["protocol_1", "protocol_2"]


def test_server_proxy_websocket_subprotocols(event_loop):
    event_loop.run_until_complete(_websocket_subprotocols())

