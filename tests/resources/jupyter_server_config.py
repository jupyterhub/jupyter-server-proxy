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
    'python-http-indexpage': {
        'command': ['python3', './tests/resources/httpinfo.py', '{port}'],
        'indexpage': 'index.html',
    },
}

import sys
sys.path.append('./tests/resources')
c.NotebookApp.nbserver_extensions = { 'proxyextension': True }
#c.Application.log_level = 'DEBUG'
