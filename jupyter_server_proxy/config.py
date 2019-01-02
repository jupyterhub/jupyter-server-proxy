"""
Traitlets based configuration for jupyter_server_proxy
"""
from notebook.utils import url_path_join as ujoin
from traitlets import Dict
from traitlets.config import Configurable
from .handlers import SuperviseAndProxyHandler, AddSlashHandler
import pkg_resources


def _make_serverproxy_handler(name, command, environment):
    """
    Create a SuperviseAndProxyHandler subclass with given parameters
    """
    # FIXME: Set 'name' properly
    class _Proxy(SuperviseAndProxyHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.name = name

        @property
        def process_args(self):
            return {
                'port': self.port
            }

        def _render_template(self, value):
            args = self.process_args
            if type(value) is str:
                return value.format(**args)
            elif type(value) is list:
                return [self._render_template(v) for v in value]
            elif type(value) is dict:
                return {
                    self._render_template(k): self._render_template(v)
                    for k, v in value.items()
                }

        def get_cmd(self):
            if callable(command):
                return self._render_template(command(**self.process_args))
            else:
                return self._render_template(command)

        def get_env(self):
            if callable(environment):
                return self._render_template(environment(**self.process_args))
            else:
                return self._render_template(environment)

    return _Proxy


def get_entrypoint_proxy_servers():
    proxy_servers = {}
    for entry_point in pkg_resources.iter_entry_points('jupyter_serverproxy_servers'):
        proxy_servers[entry_point.name] = entry_point.load()()
    return proxy_servers

def make_proxyserver_handlers(base_url, proxy_servers):
    """
    Get tornado handlers for registered proxy servers to app
    """
    handlers = []
    for name, proxy_server in proxy_servers.items():
        handler = _make_serverproxy_handler(
            name,
            proxy_server['command'],
            proxy_server.get('environment', {})
        )
        handlers.append((
            ujoin(base_url, f'{name}/(.*)'), handler, dict(state={}),
        ))
        handlers.append((
            ujoin(base_url, name), AddSlashHandler
        ))
    return handlers

class ServerProxy(Configurable):
    servers = Dict(
        {},
        help="""
        Dictionary of processes to supervise & proxy.

        Key should be the name of the process. This is also used by default as
        the URL prefix, and all requests matching this prefix are routed to this process.

        Value should be a dictionary with the following keys:
          command
            A list of strings that should be the full command to be executed. If {{port}}  is
            present, it'll be substituted with the port the process should listen on.

            Could also be a callable that takes a single argument - port. It should return
            a dictionary.

          environment
            A dictionary of environment variable mappings. {{port}} will be replaced by the port
            the process should listen on. If not explicitly set, a PORT environment variable will
            automatically be set.

            Could also be a callable that takes a single argument - port. It should return
            a dictionary.

        """,
        config=True
    )

