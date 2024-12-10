"""
Traitlets based configuration for jupyter_server_proxy
"""

import sys
from textwrap import dedent, indent
from warnings import warn

if sys.version_info < (3, 10):  # pragma: no cover
    from importlib_metadata import entry_points
else:  # pragma: no cover
    from importlib.metadata import entry_points

from jupyter_server.utils import url_path_join as ujoin
from traitlets import (
    Bool,
    Callable,
    Dict,
    Instance,
    Int,
    List,
    Tuple,
    Unicode,
    Union,
    default,
    observe,
    validate,
)
from traitlets.config import Configurable

from .handlers import AddSlashHandler, NamedLocalProxyHandler, SuperviseAndProxyHandler
from .rawsocket import RawSocketHandler, SuperviseAndRawSocketHandler


class LauncherEntry(Configurable):
    enabled = Bool(
        True,
        help="""
        Set to True (default) to make an entry in the launchers. Set to False to have no
        explicit entry.
    """,
    )

    icon_path = Unicode(
        "",
        help="""
        Full path to an svg icon that could be used with a launcher. Currently only used by the
        JupyterLab launcher
    """,
    )

    title = Unicode(
        allow_none=False,
        help="""
        Title to be used for the launcher entry. Defaults to the name of the server if missing.
    """,
    )

    path_info = Unicode(
        help="""
        The trailing path that is appended to the user's server URL to access the proxied server.
        By default it is the name of the server followed by a trailing slash.
    """,
    )

    @default("path_info")
    def _default_path_info(self):
        return self.title + "/"

    category = Unicode(
        "Notebook",
        help="""
        The category for the launcher item. Currently only used by the JupyterLab launcher.
        By default it is "Notebook".
    """,
    )


class ServerProcess(Configurable):
    name = Unicode(help="Name of the server").tag(config=True)

    command = List(
        Unicode(),
        help="""
        An optional list of strings that should be the full command to be executed.
        The optional template arguments ``{port}``, ``{unix_socket}`` and ``{base_url}``
        will be substituted with the port or Unix socket path the process should
        listen on and the base-url of the notebook.

        Could also be a callable. It should return a list.

        If the command is not specified or is an empty list, the server
        process is assumed to be started ahead of time and already available
        to be proxied to.
    """,
    ).tag(config=True)

    environment = Union(
        [Dict(Unicode()), Callable()],
        default_value={},
        help="""
        A dictionary of environment variable mappings. As with the command
        traitlet, ``{port}``, ``{unix_socket}`` and ``{base_url}`` will be substituted.

        Could also be a callable. It should return a dictionary.
    """,
    ).tag(config=True)

    timeout = Int(
        5, help="Timeout in seconds for the process to become ready, default 5s."
    ).tag(config=True)

    absolute_url = Bool(
        False,
        help="""
        Proxy requests default to being rewritten to ``/``. If this is True,
        the absolute URL will be sent to the backend instead.
    """,
    ).tag(config=True)

    port = Int(
        0,
        help="""
        Set the port that the service will listen on. The default is to automatically select an unused port.
    """,
    ).tag(config=True)

    unix_socket = Union(
        [Bool(False), Unicode()],
        default_value=None,
        allow_none=True,
        help="""
        If set, the service will listen on a Unix socket instead of a TCP port.
        Set to True to use a socket in a new temporary folder, or a string
        path to a socket. This overrides port.

        Proxying websockets over a Unix socket requires Tornado >= 6.3.
    """,
    ).tag(config=True)

    mappath = Union(
        [Dict(Unicode()), Callable()],
        default_value={},
        help="""
        Map request paths to proxied paths.
        Either a dictionary of request paths to proxied paths,
        or a callable that takes parameter ``path`` and returns the proxied path.
    """,
    ).tag(config=True)

    launcher_entry = Union(
        [Instance(LauncherEntry), Dict()],
        allow_none=False,
        help="""
        A dictionary of various options for entries in classic notebook / jupyterlab launchers.

        Keys recognized are:

            ``enabled``
                Set to True (default) to make an entry in the launchers. Set to False to have no
                explicit entry.

            ``icon_path``
                Full path to an svg icon that could be used with a launcher. Currently only used by the
                JupyterLab launcher

            ``title``
                Title to be used for the launcher entry. Defaults to the name of the server if missing.

            ``path_info``
                The trailing path that is appended to the user's server URL to access the proxied server.
                By default it is the name of the server followed by a trailing slash.

            ``category``
                The category for the launcher item. Currently only used by the JupyterLab launcher.
                By default it is "Notebook".
    """,
    ).tag(config=True)

    @validate("launcher_entry")
    def _validate_launcher_entry(self, proposal):
        kwargs = {"title": self.name}
        kwargs.update(proposal["value"])
        return LauncherEntry(**kwargs)

    @default("launcher_entry")
    def _default_launcher_entry(self):
        return LauncherEntry(title=self.name)

    new_browser_tab = Bool(
        True,
        help="""
        Set to True (default) to make the proxied server interface opened as a new browser tab. Set to False
        to have it open a new JupyterLab tab. This has no effect in classic notebook.
    """,
    ).tag(config=True)

    request_headers_override = Dict(
        Unicode(),
        default_value={},
        help="""
        A dictionary of additional HTTP headers for the proxy request. As with
        the command traitlet, ``{port}``, ``{unix_socket}`` and ``{base_url}`` will be substituted.
    """,
    ).tag(config=True)

    rewrite_response = Union(
        [Callable(), List(Callable())],
        default_value=[],
        help="""
        An optional function to rewrite the response for the given service.
        Input is a RewritableResponse object which is an argument that MUST be named
        ``response``. The function should modify one or more of the attributes
        ``.body``, ``.headers``, ``.code``, or ``.reason`` of the ``response``
        argument. For example:

        .. code-block::

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

        .. code-block::

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
    ).tag(config=True)

    progressive = Union(
        [Bool(), Callable()],
        default_value=None,
        allow_none=True,
        help="""
        Makes the proxy progressive, meaning it won't buffer any requests from the server.
        Useful for applications streaming their data, where the buffering of requests can lead
        to a lagging, e.g. in video streams.
        
        Must be either None (default), a bool, or a function. Setting it to a boolean will enable/disable 
        progressive requests for all requests. Setting to None, jupyter-server-proxy will only enable progressive 
        for somespecial types, like videos, images and binary data. A function must be taking the "Accept" header of
        the request from the client as input and returning a bool, whether this request should be made progressive.
        
        Note: `progressive` and `rewrite_response` are mutually exclusive on the same request. When rewrite_response
        is given and progressive is None, the proxying will never be progressive. If progressive is a function,
        rewrite_response will only be called on requests where it returns False. Progressive takes precedence over
        rewrite_response when both are given!
    """,
    ).tag(config=True)

    update_last_activity = Bool(
        True, help="Will cause the proxy to report activity back to jupyter server."
    ).tag(config=True)

    raw_socket_proxy = Bool(
        False,
        help="""
        Proxy websocket requests as a raw TCP (or unix socket) stream.
        In this mode, only websockets are handled, and messages are sent to the backend,
        similar to running a websockify layer (https://github.com/novnc/websockify).
        All other HTTP requests return 405 (and thus this will also bypass rewrite_response).
    """,
    ).tag(config=True)


def _make_proxy_handler(sp: ServerProcess):
    """
    Create an appropriate handler with given parameters
    """
    if sp.command:
        cls = (
            SuperviseAndRawSocketHandler
            if sp.raw_socket_proxy
            else SuperviseAndProxyHandler
        )
        args = dict(state={})
    elif not (sp.port or isinstance(sp.unix_socket, str)):
        warn(
            f"Server proxy {sp.name} does not have a command, port "
            f"number or unix_socket path. At least one of these is "
            f"required."
        )
        return
    else:
        cls = RawSocketHandler if sp.raw_socket_proxy else NamedLocalProxyHandler
        args = {}

    # FIXME: Set 'name' properly
    class _Proxy(cls):
        kwargs = args

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.name = sp.name
            self.command = sp.command
            self.proxy_base = sp.name
            self.absolute_url = sp.absolute_url
            if sp.command:
                self.requested_port = sp.port
                self.requested_unix_socket = sp.unix_socket
            else:
                self.port = sp.port
                self.unix_socket = sp.unix_socket
            self.mappath = sp.mappath
            self.rewrite_response = sp.rewrite_response
            self.progressive = sp.progressive
            self.update_last_activity = sp.update_last_activity

        def get_request_headers_override(self):
            return self._realize_rendered_template(sp.request_headers_override)

        # these two methods are only used in supervise classes, but do no harm otherwise
        def get_env(self):
            return self._realize_rendered_template(sp.environment)

        def get_timeout(self):
            return sp.timeout

    return _Proxy


def get_entrypoint_server_processes(serverproxy_config):
    sps = []
    for entry_point in entry_points(group="jupyter_serverproxy_servers"):
        name = entry_point.name
        try:
            server_process_config = entry_point.load()()
        except Exception as e:
            warn(f"entry_point {name} was unable to be loaded: {str(e)}")
            continue
        sps.append(make_server_process(name, server_process_config, serverproxy_config))
    return sps


def make_handlers(base_url, server_processes):
    """
    Get tornado handlers for registered server_processes
    """
    handlers = []
    for sp in server_processes:
        handler = _make_proxy_handler(sp)
        if not handler:
            continue
        handlers.append((ujoin(base_url, sp.name, r"(.*)"), handler, handler.kwargs))
        handlers.append((ujoin(base_url, sp.name), AddSlashHandler))
    return handlers


def make_server_process(name, server_process_config, serverproxy_config):
    return ServerProcess(name=name, **server_process_config)


def _serverproxy_servers_help():
    serverprocess_help = ""
    for k, v in ServerProcess.class_traits().items():
        help = v.metadata.get("help", "").lstrip("\n").rstrip()
        if help:
            help = indent(dedent(help), "    ")
            serverprocess_help += f"{k}\n{help}\n\n"
    return serverprocess_help


class ServerProxy(Configurable):
    servers = Dict(
        {},
        help="""
        Dictionary of processes to supervise & proxy.

        Key should be the name of the process. This is also used by default as
        the URL prefix, and all requests matching this prefix are routed to this process.

        Value should be a dictionary with the following keys:

        """
        + indent(_serverproxy_servers_help(), "        "),
        config=True,
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
        config=True,
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
        config=True,
    )

    @default("host_allowlist")
    def _host_allowlist_default(self):
        return ["localhost", "127.0.0.1"]

    host_whitelist = Union(
        trait_types=[List(), Callable()],
        help="Deprecated, use host_allowlist",
        config=True,
    )

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
