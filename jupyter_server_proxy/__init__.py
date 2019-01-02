from .handlers import setup_handlers, SuperviseAndProxyHandler
from .config import ServerProxy, make_proxyserver_handlers, get_entrypoint_proxy_servers
from notebook.utils import url_path_join as ujoin
from .api import ServersInfoHandler, LauncherEntry, IconHandler

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

    all_servers = serverproxy.servers.copy()
    all_servers.update(get_entrypoint_proxy_servers())
    server_handlers = make_proxyserver_handlers(base_url, all_servers)
    nbapp.web_app.add_handlers('.*', server_handlers)

    # Set up default handler
    setup_handlers(nbapp.web_app)

    launcher_entries = []
    icons = {}
    for name, server in all_servers.items():
        launcher_entries.append(LauncherEntry(
            name=name,
            title=server.get('title', name),
        ))
        if 'icon' in server:
            icons[name] = server['icon']

    nbapp.web_app.add_handlers('.*', [
        (ujoin(base_url, 'server-proxy/servers-info'), ServersInfoHandler, {'launcher_entries': launcher_entries}),
        (ujoin(base_url, 'server-proxy/icon/(.*)'), IconHandler, {'icons': icons})
    ])