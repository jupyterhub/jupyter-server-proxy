from .handlers import setup_handlers, SuperviseAndProxyHandler
from nbserverproxy.config import ServerProxy

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
    serverproxy = ServerProxy(parent=nbapp)
    handlers = serverproxy.get_handlers(nbapp.web_app.settings['base_url'])
    nbapp.web_app.add_handlers('.*', handlers)

    # Set up default handler
    setup_handlers(nbapp.web_app)