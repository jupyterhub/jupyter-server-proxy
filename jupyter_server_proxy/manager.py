"""Manager for jupyter server proxy"""

from collections import namedtuple

from jupyter_server.utils import url_path_join as ujoin
from tornado.ioloop import PeriodicCallback

from .utils import check_pid

ServerProxy = namedtuple("ServerProxy", ["name", "url", "cmd", "port", "managed"])
ServerProxyProc = namedtuple("ServerProxyProc", ["name", "proc"])


async def monitor_server_proxy_procs():
    """Perodically monitor the server proxy processes. If user terminates
    the process outside of jupyter-server-proxy, we should be able to
    capture that and remove proxy app from manager"""
    # Get current active apps
    procs = manager._list_server_proxy_procs()

    # Check if all pids are alive
    for proc in procs:
        exists = check_pid(proc.proc.pid)
        if not exists:
            await manager.del_server_proxy_app(proc.name)


class ServerProxyAppManager:
    """
    A class for listing and stopping server proxies that are started
    by jupyter server proxy.
    """

    def __init__(self):
        """Initialize the server proxy manager"""
        # List of server proxy apps
        self.server_proxy_apps = []

        # List of server proxy app proc objects. For internal use only
        self._server_proxy_procs = []

        # Total number of currently running proxy apps
        self.num_active_server_proxy_apps = 0

    async def add_server_proxy_app(self, name, base_url, cmd, port, proc):
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

    async def del_server_proxy_app(self, name):
        """Remove a launched proxy server from list"""
        self.server_proxy_apps = [
            app for app in self.server_proxy_apps if app.name != name
        ]
        self._server_proxy_procs = [
            app for app in self._server_proxy_procs if app.name != name
        ]
        self.num_active_server_proxy_apps -= 1

    def get_server_proxy_app(self, name):
        """Get a given server proxy app"""
        return next((app for app in self.server_proxy_apps if app.name == name), {})

    def _get_server_proxy_proc(self, name):
        """Get a given server proxy app"""
        return next((app for app in self._server_proxy_procs if app.name == name), {})

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
            await self.del_server_proxy_app(name)

            return True
        except (KeyError, AttributeError):
            return None

    async def terminate_all(self):
        """Close all server proxy and cleanup"""
        for app in self.server_proxy_apps:
            await self.terminate_server_proxy_app(app)


# Create a default manager to keep track of server proxy apps.
manager = ServerProxyAppManager()

# Create a Periodic call back function to check the status of processes
pc = PeriodicCallback(monitor_server_proxy_procs, 1e4)
pc.start()
