c.ServerProxy.servers = {
    'python-http': {
        'command': ['python3', './tests/resources/httpinfo.py', '{port}'],
    },
    'python-http-abs': {
        'command': ['python3', './tests/resources/httpinfo.py', '{port}'],
        'absolute_url': True
    },
}
#c.Application.log_level = 'DEBUG'
