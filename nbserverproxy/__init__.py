from .handlers import setup_handlers, SuperviseAndProxyHandler
from nbserverproxy.config import ServerProxy, make_proxyserver_handlers, get_entrypoint_proxy_servers

# Jupyter Extension points
def _jupyter_server_extension_paths():
    return [{
        'module': 'nbserverproxy',
    }]

def _jupyter_nbextension_paths():
    return [{
        "section": "notebook",
        "dest": "nbserverproxy",
        "require": "nbserverproxy/main"
    }]


def load_jupyter_server_extension(nbapp):
    # Set up handlers picked up via config
    base_url = nbapp.web_app.settings['base_url']
    serverproxy = ServerProxy(parent=nbapp)
    config_handlers = make_proxyserver_handlers(base_url, serverproxy.servers)
    nbapp.web_app.add_handlers('.*', config_handlers)

    entrypoint_handlers = make_proxyserver_handlers(base_url, get_entrypoint_proxy_servers())
    nbapp.web_app.add_handlers('.*', entrypoint_handlers)

    # Set up default handler
    setup_handlers(nbapp.web_app)