"""
Return config on servers to start for {{cookiecutter.project_name}}

See https://jupyter-server-proxy.readthedocs.io/en/latest/server-process.html
for more information.
"""
import os

def setup_{{cookiecutter.project_name}}():
    return {
        'command': [],
        'environment': {},
        'launcher_entry': {
            'title': '{{cookiecutter.project_name}}',
            'icon_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons', '{{cookiecutter.project_name}}.svg')
        }
    }
