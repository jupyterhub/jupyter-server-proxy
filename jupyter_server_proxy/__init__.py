import traitlets

from .api import setup_api_handlers
from .config import ServerProxy as ServerProxyConfig
from .config import get_entrypoint_server_processes, make_handlers, make_server_process
from .handlers import setup_handlers
from .manager import ServerProxyAppManager


# Jupyter Extension points
def _jupyter_server_extension_points():
    return [
        {
            "module": "jupyter_server_proxy",
        }
    ]


def _jupyter_nbextension_paths():
    return [
        {
            "section": "tree",
            "dest": "jupyter_server_proxy",
            "src": "static",
            "require": "jupyter_server_proxy/tree",
        }
    ]


def _jupyter_labextension_paths():
    return [
        {
            "src": "labextension",
            "dest": "@jupyterhub/jupyter-server-proxy",
        }
    ]


def _load_jupyter_server_extension(nbapp):
    # Set up handlers picked up via config
    base_url = nbapp.web_app.settings["base_url"]

    # Add server_proxy_manager trait to ServerApp and Instantiate a manager
    nbapp.add_traits(server_proxy_manager=traitlets.Instance(ServerProxyAppManager))
    manager = nbapp.server_proxy_manager = ServerProxyAppManager()
    serverproxy_config = ServerProxyConfig(parent=nbapp)

    # Add a long running background task that monitors the running proxies
    try:
        nbapp.io_loop.call_later(
            serverproxy_config.monitor_interval,
            manager.monitor,
            serverproxy_config.monitor_interval,
        )
    except AttributeError:
        nbapp.log.debug(
            "[jupyter-server-proxy] Server proxy manager is only supportted "
            "for Notebook >= 7",
        )

    server_processes = [
        make_server_process(name, server_process_config, serverproxy_config)
        for name, server_process_config in serverproxy_config.servers.items()
    ]
    server_processes += get_entrypoint_server_processes(serverproxy_config)
    server_handlers = make_handlers(base_url, manager, server_processes)
    nbapp.web_app.add_handlers(".*", server_handlers)

    # Set up default non-server handler
    setup_handlers(
        nbapp.web_app,
        serverproxy_config,
    )

    setup_api_handlers(
        nbapp.web_app,
        manager,
        server_processes,
    )

    nbapp.log.debug(
        "[jupyter-server-proxy] Started with known servers: %s",
        ", ".join([p.name for p in server_processes]),
    )


# For backward compatibility
load_jupyter_server_extension = _load_jupyter_server_extension
_jupyter_server_extension_paths = _jupyter_server_extension_points
