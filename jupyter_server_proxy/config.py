"""
Traitlets based configuration for jupyter_server_proxy
"""
from jupyter_server.utils import url_path_join as ujoin
from traitlets import Dict, List, Tuple, Union, default, observe
from traitlets.config import Configurable
from tornado import httpclient
from warnings import warn
from .handlers import SuperviseAndProxyHandler, AddSlashHandler, RewritableResponse
import pkg_resources
from collections import namedtuple
from .utils import call_with_asked_args

try:
    # Traitlets >= 4.3.3
    from traitlets import Callable
except ImportError:
    from .utils import Callable

def _make_serverproxy_handler(name, command, environment, timeout, absolute_url, port, mappath, request_headers_override, rewrite_response):
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
            self.rewrite_response = rewrite_response

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

        def _realize_rendered_template(self, attribute):
            '''Call any callables, then render any templated values.'''
            if callable(attribute):
                attribute = self._render_template(
                    call_with_asked_args(attribute, self.process_args)
                )
            return self._render_template(attribute)

        def get_cmd(self):
            return self._realize_rendered_template(command)

        def get_env(self):
            return self._realize_rendered_template(environment)

        def get_request_headers_override(self):
            return self._realize_rendered_template(request_headers_override)

        def get_timeout(self):
            return timeout

    return _Proxy


def get_entrypoint_server_processes(serverproxy_config):
    sps = []
    for entry_point in pkg_resources.iter_entry_points('jupyter_serverproxy_servers'):
        name = entry_point.name
        server_process_config = entry_point.load()()
        sps.append(
            make_server_process(name, server_process_config, serverproxy_config)
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
            sp.request_headers_override,
            sp.rewrite_response,
        )
        handlers.append((
            ujoin(base_url, sp.name, r'(.*)'), handler, dict(state={}),
        ))
        handlers.append((
            ujoin(base_url, sp.name), AddSlashHandler
        ))
    return handlers

LauncherEntry = namedtuple('LauncherEntry', ['enabled', 'icon_path', 'title', 'path_info'])
ServerProcess = namedtuple('ServerProcess', [
    'name', 'command', 'environment', 'timeout', 'absolute_url', 'port',
    'mappath', 'launcher_entry', 'new_browser_tab', 'request_headers_override', 'rewrite_response',
])

def make_server_process(name, server_process_config, serverproxy_config):
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
            title=le.get('title', name),
            path_info=le.get('path_info', name + "/")
        ),
        new_browser_tab=server_process_config.get('new_browser_tab', True),
        request_headers_override=server_process_config.get('request_headers_override', {}),
        rewrite_response=server_process_config.get(
            'rewrite_response',
            tuple(),
        ),
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
            A dictionary of environment variable mappings. As with the command
            traitlet, {{port}} and {{base_url}} will be substituted.

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

              path_info
                The trailing path that is appended to the user's server URL to access the proxied server.
                By default it is the name of the server followed by a trailing slash.

          new_browser_tab
            Set to True (default) to make the proxied server interface opened as a new browser tab. Set to False
            to have it open a new JupyterLab tab. This has no effect in classic notebook.

          request_headers_override
            A dictionary of additional HTTP headers for the proxy request. As with
            the command traitlet, {{port}} and {{base_url}} will be substituted.

          rewrite_response
            An optional function to rewrite the response for the given service.
            Input is a RewritableResponse object which is an argument that MUST be named
            ``response``. The function should modify one or more of the attributes
            ``.body``, ``.headers``, ``.code``, or ``.reason`` of the ``response``
            argument. For example:

                def dog_to_cat(response):
                    response.headers["I-Like"] = "tacos"
                    response.body = response.body.replace(b'dog', b'cat')

                c.ServerProxy.servers['my_server']['rewrite_response'] = dog_to_cat

            The ``rewrite_response`` function can also accept several optional
            positional arguments. Arguments named ``host``, ``port``, and ``path`` will
            receive values corresponding to the URL ``/proxy/<host>:<port><path>``. In
            addition, the original Tornado ``HTTPRequest`` and ``HTTPResponse`` objects
            are available as arguments named ``request`` and ``orig_response``. (These
            objects should not be modified.)

            A list or tuple of functions can also be specified for chaining multiple
            rewrites. For example:

                def cats_only(response, path):
                    if path.startswith("/cat-club"):
                        response.code = 403
                        response.body = b"dogs not allowed"

                c.ServerProxy.servers['my_server']['rewrite_response'] = [dog_to_cat, cats_only]

            Note that if the order is reversed to ``[cats_only, dog_to_cat]``, then accessing
            ``/cat-club`` will produce a "403 Forbidden" response with body "cats not allowed"
            instead of "dogs not allowed".

            Defaults to the empty tuple ``tuple()``.
        """,
        config=True
    )

    non_service_rewrite_response = Union(
        default_value=tuple(),
        trait_types=[List(), Tuple(), Callable()],
        help="""
        A function (or list or tuple of functions) to rewrite the response for a
        non-service request, for example a request to ``/proxy/<host>:<port><path>``.

        See the description for ``rewrite_response`` for more information.
        Defaults to the empty tuple ``tuple()``.
        """,
        config=True
    )

    host_allowlist = Union(
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

            def host_allowlist(handler, host):
                handler.log.info("Request to proxy to host " + host)
                return host.startswith("10.")
            c.ServerProxy.host_allowlist = host_allowlist

        Defaults to a list of ["localhost", "127.0.0.1"].
        """,
        config=True
    )

    @default("host_allowlist")
    def _host_allowlist_default(self):
        return ["localhost", "127.0.0.1"]

    host_whitelist = Union(
        trait_types=[List(), Callable()],
        help="Deprecated, use host_allowlist",
        config=True)

    @observe("host_whitelist")
    def _host_whitelist_deprecated(self, change):
        old_attr = change.name
        if self.host_allowlist != change.new:
            # only warn if different
            # protects backward-compatible config from warnings
            # if they set the same value under both names
            # Configurable doesn't have a log
            # https://github.com/ipython/traitlets/blob/5.0.5/traitlets/config/configurable.py#L181
            warn(
                "{cls}.{old} is deprecated in jupyter-server-proxy {version}, use {cls}.{new} instead".format(
                    cls=self.__class__.__name__,
                    old=old_attr,
                    new="host_allowlist",
                    version="3.0.0",
                )
            )
            self.host_allowlist = change.new
