"""
Traitlets based configuration for jupyter_server_proxy
"""
from notebook.utils import url_path_join as ujoin
from traitlets import Dict, List, Union, default
from traitlets.config import Configurable
from .handlers import SuperviseAndProxyHandler, AddSlashHandler
import pkg_resources
from collections import namedtuple
from .utils import call_with_asked_args

try:
    # Traitlets >= 4.3.3
    from traitlets import Callable
except ImportError:
    from .utils import Callable

def _make_serverproxy_handler(name, command, environment, timeout, absolute_url, port, mappath):
    """
    Create a SuperviseAndProxyHandler subclass with given parameters
    """
    # FIXME: Set 'name' properly
    class _Proxy(SuperviseAndProxyHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.name = name
            self.proxy_base = name
            self.absolute_url = absolute_url
            self.requested_port = port
            self.mappath = mappath

        @property
        def process_args(self):
            return {
                'port': self.port,
                'base_url': self.base_url,
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
            else:
                raise ValueError('Value of unrecognized type {}'.format(type(value)))

        def get_cmd(self):
            if callable(command):
                return self._render_template(call_with_asked_args(command, self.process_args))
            else:
                return self._render_template(command)

        def get_env(self):
            if callable(environment):
                return self._render_template(call_with_asked_args(environment, self.process_args))
            else:
                return self._render_template(environment)

        def get_timeout(self):
            return timeout

    return _Proxy


def get_entrypoint_server_processes():
    sps = []
    for entry_point in pkg_resources.iter_entry_points('jupyter_serverproxy_servers'):
        sps.append(
            make_server_process(entry_point.name, entry_point.load()())
        )
    return sps

def make_handlers(base_url, server_processes):
    """
    Get tornado handlers for registered server_processes
    """
    handlers = []
    for sp in server_processes:
        handler = _make_serverproxy_handler(
            sp.name,
            sp.command,
            sp.environment,
            sp.timeout,
            sp.absolute_url,
            sp.port,
            sp.mappath,
        )
        handlers.append((
            ujoin(base_url, sp.name, r'(.*)'), handler, dict(state={}),
        ))
        handlers.append((
            ujoin(base_url, sp.name), AddSlashHandler
        ))
    return handlers

LauncherEntry = namedtuple('LauncherEntry', ['enabled', 'icon_path', 'title'])
ServerProcess = namedtuple('ServerProcess', [
    'name', 'command', 'environment', 'timeout', 'absolute_url', 'port', 'mappath', 'launcher_entry', 'new_browser_tab'])

def make_server_process(name, server_process_config):
    le = server_process_config.get('launcher_entry', {})
    return ServerProcess(
        name=name,
        command=server_process_config['command'],
        environment=server_process_config.get('environment', {}),
        timeout=server_process_config.get('timeout', 5),
        absolute_url=server_process_config.get('absolute_url', False),
        port=server_process_config.get('port', 0),
        mappath=server_process_config.get('mappath', {}),
        launcher_entry=LauncherEntry(
            enabled=le.get('enabled', True),
            icon_path=le.get('icon_path'),
            title=le.get('title', name)
        ),
        new_browser_tab=server_process_config.get('new_browser_tab', True)
    )

class ServerProxy(Configurable):
    servers = Dict(
        {},
        help="""
        Dictionary of processes to supervise & proxy.

        Key should be the name of the process. This is also used by default as
        the URL prefix, and all requests matching this prefix are routed to this process.

        Value should be a dictionary with the following keys:
          command
            A list of strings that should be the full command to be executed.
            The optional template arguments {{port}} and {{base_url}} will be substituted with the
            port the process should listen on and the base-url of the notebook.

            Could also be a callable. It should return a list.

          environment
            A dictionary of environment variable mappings. {{port}} and {{base_url}} will be
            substituted as for command.

            Could also be a callable. It should return a dictionary.

          timeout
            Timeout in seconds for the process to become ready, default 5s.

          absolute_url
            Proxy requests default to being rewritten to '/'. If this is True,
            the absolute URL will be sent to the backend instead.

          port
            Set the port that the service will listen on. The default is to automatically select an unused port.

          mappath
            Map request paths to proxied paths.
            Either a dictionary of request paths to proxied paths,
            or a callable that takes parameter ``path`` and returns the proxied path.

          launcher_entry
            A dictionary of various options for entries in classic notebook / jupyterlab launchers.

            Keys recognized are:

            enabled
              Set to True (default) to make an entry in the launchers. Set to False to have no
              explicit entry.

            icon_path
              Full path to an svg icon that could be used with a launcher. Currently only used by the
              JupyterLab launcher

            title
              Title to be used for the launcher entry. Defaults to the name of the server if missing.

          new_browser_tab
            Set to True (default) to make the proxied server interface opened as a new browser tab. Set to False
            to have it open a new JupyterLab tab. This has no effect in classic notebook.
        """,
        config=True
    )

    host_whitelist = Union(
        trait_types=[List(), Callable()],
        help="""
        List of allowed hosts.
        Can also be a function that decides whether a host can be proxied.

        If implemented as a function, this should return True if a host should
        be proxied and False if it should not.  Such a function could verify
        that the host matches a particular regular expression pattern or falls
        into a specific subnet.  It should probably not be a slow check against
        some external service.  Here is an example that could be placed in a
        site-wide Jupyter notebook config:

            def host_whitelist(handler, host):
                handler.log.info("Request to proxy to host " + host)
                return host.startswith("10.")
            c.ServerProxy.host_whitelist = host_whitelist

        Defaults to a list of ["localhost", "127.0.0.1"].
        """,
        config=True
    )

    @default("host_whitelist")
    def _host_whitelist_default(self):
        return ["localhost", "127.0.0.1"]
