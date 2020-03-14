import os
from http.client import HTTPConnection
from urllib.parse import quote
import pytest

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


def test_server_proxy_url_encoding():
    special_path = quote('Hellö Wörld 🎉你好世界@±¥')
    test_url = '/python-http/' + special_path
    r = request_get(PORT, test_url, TOKEN)
    assert r.code == 200
    s = r.read().decode('ascii')
    assert s.startswith('GET /{}?token='.format(special_path))


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
