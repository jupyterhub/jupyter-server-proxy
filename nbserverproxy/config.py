"""
Traitlets based configuration for nbserverproxy
"""
from notebook.utils import url_path_join as ujoin
from traitlets import Float, Int, Dict
from traitlets.config import Configurable
from nbserverproxy.handlers import SuperviseAndProxyHandler, AddSlashHandler


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

          environment
            A dictionary of environment variable mappings. {{port}} will be replaced by the port
            the process should listen on. If not explicitly set, a PORT environment variable will
            automatically be set.

        """,
        config=True
    )

    def _make_serverproxy_handler(self, name):
        """
        Create a Tornado handler class for server with this name
        """
        proxy_server = self.servers[name]

        # FIXME: Set 'name' properly
        class _Proxy(SuperviseAndProxyHandler):
            def _render_template(self, value):
                args = {
                    'port': self.port
                }
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
                return self._render_template(proxy_server['command'])
            
            def get_env(self):
                return self._render_template(proxy_server.get('environment', {}))
        
        return _Proxy


    def get_handlers(self, base_url):
        """
        Get tornado handlers for registered proxy servers to app
        """
        handlers = []
        for name in self.servers:
            handlers.append((
                ujoin(base_url, f'{name}/(.*)'), self._make_serverproxy_handler(name), dict(state={}),
            ))
            self.log.debug(f'Adding handler for server {name}')
            handlers.append((
                ujoin(base_url, name), AddSlashHandler
            ))
        return handlers
