"""
Traitlets based configuration for jupyter_server_proxy
"""

from __future__ import annotations

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
    Float,
    HasTraits,
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


class LauncherEntry(HasTraits):
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

    category = Unicode(
        "Notebook",
        help="""
        The category for the launcher item. Currently only used by the JupyterLab launcher.
        By default it is "Notebook".
    """,
    )


class ServerProcess(Configurable):
    name = Unicode(help="Name of the server")

    command = Union(
        [List(Unicode()), Callable()],
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
    )

    environment = Union(
        [Dict(Unicode()), Callable()],
        default_value={},
        help="""
        A dictionary of environment variable mappings. As with the command
        traitlet, ``{port}``, ``{unix_socket}`` and ``{base_url}`` will be substituted.

        Could also be a callable. It should return a dictionary.
    """,
    ).tag(config=True)

    timeout = Float(
        5.0, help="Timeout in seconds for the process to become ready, default 5s."
    ).tag(config=True)

    absolute_url = Bool(
        False,
        help="""
        Proxy requests default to being rewritten to ``/``. If this is True,
        the absolute URL will be sent to the backend instead.
    """,
    )

    port = Int(
        0,
        help="""
        Set the port that the service will listen on. The default is to automatically select an unused port.
    """,
    )

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
    )

    mappath = Union(
        [Dict(Unicode()), Callable()],
        default_value={},
        help="""
        Map request paths to proxied paths.
        Either a dictionary of request paths to proxied paths,
        or a callable that takes parameter ``path`` and returns the proxied path.
    """,
    )

    launcher_entry = Union(
        [Instance(LauncherEntry), Dict()],
        allow_none=False,
        help="""
        Specify various options for entries in classic notebook / jupyterlab launchers.

        Must be an instance of ``LauncherEntry`` or a dictionary with the following keys:

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
    )

    @validate("launcher_entry")
    def _validate_launcher_entry(self, proposal):
        if isinstance(proposal["value"], LauncherEntry):
            proposal["value"].title = self.name
            proposal["value"].path_info = self.name + "/"
            return proposal["value"]
        else:
            kwargs = {"title": self.name, "path_info": self.name + "/"}
            kwargs.update(proposal["value"])
            return LauncherEntry(**kwargs)

    @default("launcher_entry")
    def _default_launcher_entry(self):
        return LauncherEntry(title=self.name, path_info=self.name + "/")

    new_browser_tab = Bool(
        True,
        help="""
        Set to True (default) to make the proxied server interface opened as a new browser tab. Set to False
        to have it open a new JupyterLab tab. This has no effect in classic notebook.
    """,
    ).tag(config=True)

    request_headers_override = Union(
        [Dict(Unicode()), Callable()],
        default_value={},
        help="""
        A dictionary of additional HTTP headers for the proxy request. As with
        the command traitlet, ``{port}``, ``{unix_socket}`` and ``{base_url}`` will be substituted.
    """,
    )

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
    )

    def get_proxy_base_class(self) -> tuple[type | None, dict]:
        """
        Return the appropriate ProxyHandler Subclass and its kwargs
        """
        if self.command:
            return (
                SuperviseAndRawSocketHandler
                if self.raw_socket_proxy
                else SuperviseAndProxyHandler
            ), dict(state={})

        if not (self.port or isinstance(self.unix_socket, str)):
            warn(
                f"""Server proxy {self.name} does not have a command, port number or unix_socket path. 
                At least one of these is required."""
            )
            return None, dict()

        return (
            RawSocketHandler if self.raw_socket_proxy else NamedLocalProxyHandler
        ), dict()

    def get_proxy_attributes(self) -> dict:
        """
        Return the required attributes, which will be set on the proxy handler
        """
        attributes = {
            "name": self.name,
            "command": self.command,
            "proxy_base": self.name,
            "absolute_url": self.absolute_url,
            "mappath": self.mappath,
            "rewrite_response": self.rewrite_response,
            "update_last_activity": self.update_last_activity,
            "request_headers_override": self.request_headers_override,
        }

        if self.command:
            attributes["requested_port"] = self.port
            attributes["requested_unix_socket"] = self.unix_socket
            attributes["environment"] = self.environment
            attributes["timeout"] = self.timeout
        else:
            attributes["port"] = self.port
            attributes["unix_socket"] = self.unix_socket

        return attributes

    def make_proxy_handler(self) -> tuple[type | None, dict]:
        """
        Create an appropriate handler for this ServerProxy Configuration
        """
        cls, proxy_kwargs = self.get_proxy_base_class()
        if cls is None:
            return None, proxy_kwargs

        # FIXME: Set 'name' properly
        attributes = self.get_proxy_attributes()

        class _Proxy(cls):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                for name, value in attributes.items():
                    setattr(self, name, value)

            def get_request_headers_override(self):
                return self._realize_rendered_template(self.request_headers_override)

            # these two methods are only used in supervise classes, but do no harm otherwise
            def get_env(self):
                return self._realize_rendered_template(self.environment)

            def get_timeout(self):
                return self.timeout

        return _Proxy, proxy_kwargs


def get_entrypoint_server_processes():
    processes = []
    for entry_point in entry_points(group="jupyter_serverproxy_servers"):
        name = entry_point.name
        try:
            server_process_config = entry_point.load()()
        except Exception as e:
            warn(f"entry_point {name} was unable to be loaded: {str(e)}")
            continue
        processes.append(ServerProcess(name=name, **server_process_config))
    return processes


def make_handlers(base_url: str, server_processes: list[ServerProcess]):
    """
    Get tornado handlers for registered server_processes
    """
    handlers = []
    for server in server_processes:
        handler, kwargs = server.make_proxy_handler()
        if not handler:
            continue
        handlers.append((ujoin(base_url, server.name, r"(.*)"), handler, kwargs))
        handlers.append((ujoin(base_url, server.name), AddSlashHandler))
    return handlers


def make_server_process(name: str, server_process_config: dict, serverproxy_config):
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
        key_trait=Unicode(),
        value_trait=Union([Dict(), Instance(ServerProcess)]),
        help="""
        Dictionary of processes to supervise & proxy.

        Key should be the name of the process. This is also used by default as
        the URL prefix, and all requests matching this prefix are routed to this process.

        Value should be an instance of ``ServerProcess`` or a dictionary with the following keys:

        """
        + indent(_serverproxy_servers_help(), "        "),
        config=True,
    )

    @validate("servers")
    def _validate_servers(self, proposal):
        servers = {}

        for name, server_process in proposal["value"].items():
            if isinstance(server_process, ServerProcess):
                server_process.name = server_process.name or name
                servers[name] = server_process
            else:
                kwargs = {"name": name}
                kwargs.update(**server_process)
                servers[name] = ServerProcess(**kwargs)

        return servers

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
