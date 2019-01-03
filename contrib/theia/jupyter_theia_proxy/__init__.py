"""
Return config on servers to start for theia

See https://jupyter-server-proxy.readthedocs.io/en/latest/server-process.html
for more information.
"""
import os
import shutil

def setup_theia():
    # Make sure theia is in $PATH
    def _theia_command(port):
        full_path = shutil.which('theia')
        if not full_path:
            raise FileNotFoundError('Can not find theia executable in $PATH')
        return ['theia', 'start', '.', '--hostname=127.0.0.1', '--port=' + str(port)]

    return {
        'command': _theia_command,
        'environment': {
            'USE_LOCAL_GIT': 'true'
        },
        'launcher_entry': {
            'title': 'Theia IDE',
            'icon_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons', 'theia.svg')
        }
    }