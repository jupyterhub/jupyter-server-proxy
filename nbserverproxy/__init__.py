from .handlers import setup_handlers, SuperviseAndProxyHandler
from nbserverproxy.config import ServerProxy, make_proxyserver_handlers, get_entrypoint_proxy_servers
from notebook.utils import url_path_join as ujoin
from nbserverproxy.api import ServersInfoHandler, LauncherEntry

# Jupyter Extension points
def _jupyter_server_extension_paths():
    return [{
        'module': 'nbserverproxy',
    }]

def _jupyter_nbextension_paths():
    return [{
        "section": "tree",
        "dest": "nbserverproxy",
        'src': 'static',
        "require": "nbserverproxy/tree"
    }]


def load_jupyter_server_extension(nbapp):
    # Set up handlers picked up via config
    base_url = nbapp.web_app.settings['base_url']
    serverproxy = ServerProxy(parent=nbapp)
    config_handlers = make_proxyserver_handlers(base_url, serverproxy.servers)
    nbapp.web_app.add_handlers('.*', config_handlers)

    entrypoint_servers = get_entrypoint_proxy_servers()
    entrypoint_handlers = make_proxyserver_handlers(base_url, entrypoint_servers)
    nbapp.web_app.add_handlers('.*', entrypoint_handlers)

    # Set up default handler
    setup_handlers(nbapp.web_app)

    launcher_entries = []
    for name, server in serverproxy.servers.items():
        launcher_entries.append(LauncherEntry(name=name, title=server.get('title', name)))

    for name, server in entrypoint_servers.items():
        launcher_entries.append(LauncherEntry(name=name, title=server.get('title', name)))

    nbapp.web_app.add_handlers('.*', [
        (ujoin(base_url, 'server-proxy/servers-info'), ServersInfoHandler, {'launcher_entries': launcher_entries})
    ])