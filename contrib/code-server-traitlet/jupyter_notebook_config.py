c.ServerProxy.servers = {
  'code-server': {
    'command': [
      'code-server',
        '--auth=none',
        '--disable-telemetry',
        '--bind-addr=localhost:{port}'
    ],
    'timeout': 20,
    'launcher_entry': {
      'title': 'VS Code'
    }
  }
}
