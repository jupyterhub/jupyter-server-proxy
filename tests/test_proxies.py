import asyncio
import gzip
from io import BytesIO
import json
import os
from http.client import HTTPConnection
from urllib.parse import quote
import pytest
from tornado.httpclient import HTTPClientError
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
    special_path = quote("Hello world 123 åäö 🎉你好世界±¥ :/[]@!$&'()*+,;=-._~?key1=value1", safe=":/?#[]@!$&'()*+,;=-._~")
    test_url = '/python-http/' + special_path
    r = request_get(PORT, test_url, TOKEN)
    assert r.code == 200
    s = r.read().decode('ascii')
    assert 'GET /{}&token='.format(special_path) in s


def test_server_proxy_hash_sign_encoding():
    """
    FIXME: This is a test to establish the current behavior, but if it should be
           like this is a separate question not yet addressed.

           Related: https://github.com/jupyterhub/jupyter-server-proxy/issues/109
    """
    h = HTTPConnection("localhost", PORT, 10)

    # Case 0: a reference case
    path = "?token={}".format(TOKEN)
    h.request('GET', '/python-http/' + path)
    r = h.getresponse()
    assert r.code == 200
    s = r.read().decode('ascii')
    assert 'GET /{} '.format(path) in s

    # Case 1: #bla?token=secret -> everything following # ignored -> redirect because no token
    path = "#bla?token={}".format(TOKEN)
    h.request('GET', '/python-http/' + path)
    r = h.getresponse()
    assert r.code == 200
    s = r.read().decode('ascii')
    assert 'GET / ' in s

    # Case 2: %23bla?token=secret -> %23 is # -> everything following # ignored -> redirect because no token
    path = "%23?token={}".format(TOKEN)
    h.request('GET', '/python-http/' + path)
    r = h.getresponse()
    assert r.code == 200
    s = r.read().decode('ascii')
    assert 'GET / ' in s

    # Case 3: ?token=secret#test -> invalid token -> jupyter notebook server errors: NoneType can't be used in 'await' expression
    #
    #   [E 11:37:49.991 NotebookApp] Uncaught exception GET /python-http/?token=secrettest (127.0.0.1)
    #   HTTPServerRequest(protocol='http', host='localhost:8888', method='GET', uri='/python-http/?token=secrettest', version='HTTP/1.1', remote_ip='127.0.0.1')
    #   Traceback (most recent call last):
    #   File "/home/erik/py/lib/python3.7/site-packages/tornado/web.py", line 1704, in _execute
    #       result = await result
    #   File "/home/erik/py/lib/python3.7/site-packages/jupyter_server_proxy/websocket.py", line 97, in get
    #       return await self.http_get(*args, **kwargs)
    #   File "/home/erik/py/lib/python3.7/site-packages/jupyter_server_proxy/handlers.py", line 539, in http_get
    #       return await self.proxy(self.port, path)
    #   TypeError: object NoneType can't be used in 'await' expression
    path = "?token={}#test".format(TOKEN)
    h.request('GET', '/python-http/' + path)
    r = h.getresponse()
    assert r.code == 302
    s = r.read().decode('ascii')
    assert s == ''


def test_server_rewrite_response():
    r = request_get(PORT, '/python-http-rewrite-response/ciao-a-tutti', TOKEN)
    assert r.code == 418
    assert r.reason == "I'm a teapot"
    assert ("I-Like", "tacos") in r.headers.items()
    assert ("Proxied-Host-Port", "localhost:54323") in r.headers.items()
    assert ("Proxied-Path", "/ciao-a-tutti") in r.headers.items()
    s = r.read().decode('ascii')
    assert s.startswith('GET /hello-a-tutti?token=')


def test_chained_rewrite_response():
    r = request_get(PORT, '/python-chained-rewrite-response/ciao-a-tutti', TOKEN)
    assert r.code == 418
    assert r.reason == "I'm a teapot"
    s = r.read().decode('ascii')
    assert s.startswith('GET /foo-a-tutti?token=')


def test_cats_and_dogs_rewrite_response():
    r = request_get(PORT, '/python-cats-only-rewrite-response/goats', TOKEN)
    assert r.code == 200
    r = request_get(PORT, '/python-cats-only-rewrite-response/cat-club', TOKEN)
    s = r.read().decode('ascii')
    assert r.code == 403
    assert r.reason == "Forbidden"
    assert s == "dogs not allowed"
    r = request_get(PORT, '/python-dogs-only-rewrite-response/cat-club', TOKEN)
    s = r.read().decode('ascii')
    assert r.code == 403
    assert r.reason == "Forbidden"
    assert s == "cats not allowed"


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


def test_server_proxy_host_non_absolute():
    # note: localhost: is stripped but 127.0.0.1: is not
    r = request_get(PORT, '/proxy/127.0.0.1:54321/jkl', TOKEN)
    assert r.code == 200
    s = r.read().decode('ascii')
    assert s.startswith('GET /jkl?token=')
    assert 'X-Forwarded-Context: /proxy/127.0.0.1:54321\n' in s
    assert 'X-Proxycontextpath: /proxy/127.0.0.1:54321\n' in s


def test_server_proxy_host_absolute():
    r = request_get(PORT, '/proxy/absolute/127.0.0.1:54321/nmo', TOKEN)
    assert r.code == 200
    s = r.read().decode('ascii')
    assert s.startswith('GET /proxy/absolute/127.0.0.1:54321/nmo?token=')
    assert 'X-Forwarded-Context' not in s
    assert 'X-Proxycontextpath' not in s


@pytest.mark.parametrize("absolute", ["", "/absolute"])
def test_server_proxy_host_invalid(absolute: str) -> None:
    r = request_get(PORT, f"/proxy{absolute}/<invalid>:54321/", TOKEN)
    assert r.code == 403
    s = r.read().decode("ascii")
    assert "Host &#39;&lt;invalid&gt;&#39; is not allowed." in s


def test_server_proxy_port_non_service_rewrite_response():
    """Test that 'hello' is replaced by 'foo'."""
    r = request_get(PORT, '/proxy/54321/hello', TOKEN)
    assert r.code == 200
    s = r.read().decode('ascii')
    assert s.startswith('GET /foo?token=')


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


def test_server_request_headers():
    r = request_get(PORT, '/python-request-headers/', TOKEN, host='127.0.0.1')
    assert r.code == 200
    s = r.read().decode('ascii')
    assert 'X-Custom-Header: pytest-23456\n' in s


def test_server_content_encoding_header():
    r = request_get(PORT, '/python-gzipserver/', TOKEN, host='127.0.0.1')
    assert r.code == 200
    assert r.headers['Content-Encoding'] == 'gzip'
    with gzip.GzipFile(fileobj=BytesIO(r.read()), mode='r') as f:
        assert f.read() == b'this is a test'


@pytest.mark.asyncio
async def test_server_proxy_websocket_messages():
    url = "ws://localhost:{}/python-websocket/echosocket?token={}".format(PORT, TOKEN)
    conn = await websocket_connect(url)
    expected_msg = "Hello, world!"
    await conn.write_message(expected_msg)
    msg = await conn.read_message()
    assert msg == expected_msg


@pytest.mark.asyncio
async def test_server_proxy_websocket_headers():
    url = "ws://localhost:{}/python-websocket/headerssocket?token={}".format(PORT, TOKEN)
    conn = await websocket_connect(url)
    await conn.write_message("Hello")
    msg = await conn.read_message()
    headers = json.loads(msg)
    assert 'X-Custom-Header' in headers
    assert headers['X-Custom-Header'] == 'pytest-23456'


@pytest.mark.asyncio
async def test_server_proxy_websocket_subprotocols():
    url = "ws://localhost:{}/python-websocket/subprotocolsocket?token={}".format(PORT, TOKEN)
    conn = await websocket_connect(url, subprotocols=["protocol_1", "protocol_2"])
    await conn.write_message("Hello, world!")
    msg = await conn.read_message()
    assert json.loads(msg) == ["protocol_1", "protocol_2"]


@pytest.mark.asyncio
async def test_websocket_no_auth_failure():
    # Intentionally do not pass an appropriate token, which should cause a 403
    url = "ws://localhost:{}/python-websocket/headerssocket".format(PORT)

    with pytest.raises(HTTPClientError, match=r".*HTTP 403: Forbidden.*"):
        await websocket_connect(url)


@pytest.mark.parametrize(
    "proxy_path, status",
    [
        ("127.0.0.1", 404),
        ("127.0.0.1/path", 404),
        ("127.0.0.1@192.168.1.1", 404),
        ("127.0.0.1@192.168.1.1/path", 404),
        ("user:pass@host:123/foo", 404),
        ("user:pass@host/foo", 404),
        ("absolute/127.0.0.1:123@192.168.1.1/path", 404),
    ]
)
def test_bad_server_proxy_url(proxy_path, status):
    r = request_get(PORT, f"/proxy/{proxy_path}", TOKEN)
    assert r.code == status
    if status >= 400:
        # request should not have been proxied
        assert 'X-ProxyContextPath' not in r.headers
