import os
from http.client import HTTPConnection

PORT = os.getenv('TEST_PORT', 8888)
TOKEN = os.getenv('JUPYTER_TOKEN', 'secret')


def request_get(port, path, token):
    h = HTTPConnection('localhost', port, 10)
    h.request('GET', '{}?token={}'.format(path, token))
    return h.getresponse()


def test_server_proxy_rewrite():
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
