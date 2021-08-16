def mappathf(path):
    p = path + 'mapped'
    return p

c.ServerProxy.servers = {
    'python-http': {
        'command': ['python3', './tests/resources/httpinfo.py', '{port}'],
    },
    'python-http-abs': {
        'command': ['python3', './tests/resources/httpinfo.py', '{port}'],
        'absolute_url': True
    },
    'python-http-port54321': {
        'command': ['python3', './tests/resources/httpinfo.py', '{port}'],
        'port': 54321,
    },
    'python-http-mappath': {
        'command': ['python3', './tests/resources/httpinfo.py', '{port}'],
        'mappath': {
            '/': '/index.html',
        }
    },
    'python-http-mappathf': {
        'command': ['python3', './tests/resources/httpinfo.py', '{port}'],
        'mappath': mappathf,
    },
    'python-websocket' : {
        'command': ['python3', './tests/resources/websocket.py', '--port={port}'],
    },
    'python-request-headers': {
        'command': ['python3', './tests/resources/httpinfo.py', '{port}'],
        'request_headers_override': {
            'X-Custom-Header': 'pytest-23456',
        }
    }
}

import sys
sys.path.append('./tests/resources')
c.ServerApp.jpserver_extensions = { 'proxyextension': True }
c.NotebookApp.nbserver_extensions = { 'proxyextension': True }
#c.Application.log_level = 'DEBUG'
