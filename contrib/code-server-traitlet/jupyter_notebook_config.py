c.ServerProxy.servers = {
  'code-server': {
    'command': [
      'code-server',
        '--no-auth',
        '--disable-telemetry',
        '--allow-http',
        '--port={port}'
    ],
    'timeout': 20,
    'launcher_entry': {
      'title': 'VS Code'
    }
  }
}
