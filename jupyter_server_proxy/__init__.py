from .handlers import setup_handlers, SuperviseAndProxyHandler
from .config import ServerProxy, make_handlers, get_entrypoint_server_processes, make_server_process
from notebook.utils import url_path_join as ujoin
from .api import ServersInfoHandler, IconHandler

# Jupyter Extension points
def _jupyter_server_extension_paths():
    return [{
        'module': 'jupyter_server_proxy',
    }]

def _jupyter_nbextension_paths():
    return [{
        "section": "tree",
        "dest": "jupyter_server_proxy",
        'src': 'static',
        "require": "jupyter_server_proxy/tree"
    }]


def load_jupyter_server_extension(nbapp):
    # Set up handlers picked up via config
    base_url = nbapp.web_app.settings['base_url']
    serverproxy = ServerProxy(parent=nbapp)

    server_proccesses = [make_server_process(k, v) for k, v in serverproxy.servers.items()]
    server_proccesses += get_entrypoint_server_processes()
    server_handlers = make_handlers(base_url, server_proccesses)
    nbapp.web_app.add_handlers('.*', server_handlers)

    # Set up default handler
    setup_handlers(nbapp.web_app, serverproxy.host_whitelist)

    launcher_entries = []
    icons = {}
    for sp in server_proccesses:
        if sp.launcher_entry.enabled and sp.launcher_entry.icon_path:
            icons[sp.name] = sp.launcher_entry.icon_path

    nbapp.web_app.add_handlers('.*', [
        (ujoin(base_url, 'server-proxy/servers-info'), ServersInfoHandler, {'server_processes': server_proccesses}),
        (ujoin(base_url, 'server-proxy/icon/(.*)'), IconHandler, {'icons': icons})
    ])
