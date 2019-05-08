import os
from http.client import HTTPConnection

PORT = os.getenv('TEST_PORT', 8888)
TOKEN = os.getenv('JUPYTER_TOKEN', 'secret')


def request_get(port, path, token, host='localhost'):
    h = HTTPConnection(host, port, 10)
    h.request('GET', '{}?token={}'.format(path, token))
    return h.getresponse()


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

def test_server_proxy_remote():
    r = request_get(PORT, '/newproxy', TOKEN, host='127.0.0.1')
    assert r.code == 200
