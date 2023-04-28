"""Manager for jupyter server proxy"""

import asyncio
from collections import namedtuple

from jupyter_server.utils import url_path_join as ujoin
from traitlets import Int, List
from traitlets.config import LoggingConfigurable

ServerProxy = namedtuple(
    "ServerProxy",
    ["name", "url", "cmd", "port", "managed", "unix_socket"],
    defaults=[""] * 6,
)
ServerProxyProc = namedtuple("ServerProxyProc", ["name", "proc"], defaults=[""] * 2)


class ServerProxyAppManager(LoggingConfigurable):
    """
    A class for listing and stopping server proxies that are started
    by jupyter server proxy.
    """

    server_proxy_apps = List(help="List of server proxy apps")

    _server_proxy_procs = List(help="List of server proxy app proc objects")

    num_active_server_proxy_apps = Int(
        0, help="Total number of currently running proxy apps"
    )

    def add_server_proxy_app(self, name, base_url, cmd, port, proc, unix_socket):
        """Add a launched proxy server to list"""
        self.num_active_server_proxy_apps += 1

        # Add proxy server metadata
        self.server_proxy_apps.append(
            ServerProxy(
                name=name,
                url=ujoin(base_url, name),
                cmd=" ".join(cmd),
                port=port,
                managed=True if proc else False,
                unix_socket=unix_socket if unix_socket is not None else "",
            )
        )

        # Add proxy server proc object so that we can send SIGTERM
        # when user chooses to shut it down
        self._server_proxy_procs.append(
            ServerProxyProc(
                name=name,
                proc=proc,
            )
        )
        self.log.debug("Server proxy %s added to server proxy manager" % name)

    def del_server_proxy_app(self, name):
        """Remove a launched proxy server from list"""
        self.server_proxy_apps = [
            app for app in self.server_proxy_apps if app.name != name
        ]
        self._server_proxy_procs = [
            app for app in self._server_proxy_procs if app.name != name
        ]
        self.num_active_server_proxy_apps = len(self.server_proxy_apps)

    def get_server_proxy_app(self, name):
        """Get a given server proxy app"""
        return next(
            (app for app in self.server_proxy_apps if app.name == name), ServerProxy()
        )

    def _get_server_proxy_proc(self, name):
        """Get a given server proxy app"""
        return next(
            (app for app in self._server_proxy_procs if app.name == name),
            ServerProxyProc(),
        )

    def list_server_proxy_apps(self):
        """List all active server proxy apps"""
        return self.server_proxy_apps

    def _list_server_proxy_procs(self):
        """List all active server proxy proc objs"""
        return self._server_proxy_procs

    async def terminate_server_proxy_app(self, name):
        """Terminate a server proxy by sending SIGTERM"""
        app = self._get_server_proxy_proc(name)
        try:
            # Here we send SIGTERM signal to terminate proxy app
            # graciously so we can restart it if needed. Note that
            # some servers may not get stopped by sending SIGTERM
            # signal (example is mlflow server). In this case, it is
            # user's responsibility to write wrapper scripts around
            # proxy app's executable to terminate them cleanly using
            # TERM signal. It is also important to set exit code to 0
            # when using such wrappers when proxy apps shutdown.
            await app.proc.terminate()

            # Remove proxy app from list
            self.del_server_proxy_app(name)

            self.log.debug("Server proxy %s removed from server proxy manager" % name)

            return True
        except (KeyError, AttributeError):
            self.log.warning("Server proxy %s not found in server proxy manager" % name)
            return None

    async def terminate_all(self):
        """Close all server proxy and cleanup"""
        for app in self.server_proxy_apps:
            await self.terminate_server_proxy_app(app)

    async def monitor(self, monitor_interval):
        while True:
            procs = self._list_server_proxy_procs()

            # Check if processes are running
            for proc in procs:
                running = proc.proc.running
                if not running:
                    self.log.warning(
                        "Server proxy %s is not running anymore. "
                        "Removing from server proxy manager" % proc.name
                    )
                    self.del_server_proxy_app(proc.name)

            await asyncio.sleep(monitor_interval)
