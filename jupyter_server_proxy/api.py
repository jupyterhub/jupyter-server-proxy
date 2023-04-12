import json

from jupyter_server.base.handlers import JupyterHandler
from jupyter_server.utils import url_path_join as ujoin
from tornado import web

from .manager import manager


class ServersInfoHandler(JupyterHandler):
    def initialize(self, server_processes):
        self.server_processes = server_processes

    @web.authenticated
    async def get(self):
        data = []
        # Pick out and send only metadata
        # Don't send anything that might be a callable, or leak sensitive info
        for sp in self.server_processes:
            # Manually recurse to convert namedtuples into JSONable structures
            item = {
                "name": sp.name,
                "launcher_entry": {
                    "enabled": sp.launcher_entry.enabled,
                    "title": sp.launcher_entry.title,
                    "path_info": sp.launcher_entry.path_info,
                },
                "new_browser_tab": sp.new_browser_tab,
            }
            if sp.launcher_entry.icon_path:
                icon_url = ujoin(self.base_url, "server-proxy", "icon", sp.name)
                item["launcher_entry"]["icon_url"] = icon_url

            data.append(item)

        self.write({"server_processes": data})


# Took it from JupyterHub LogoHandler
class IconHandler(web.StaticFileHandler):
    """A singular handler for serving the icon."""

    def get(self):
        return super().get("")

    @classmethod
    def get_absolute_path(cls, root, path):
        """We only serve one file, ignore relative path"""
        import os

        return os.path.abspath(root)


class ServersAPIHandler(JupyterHandler):
    """Handler to get metadata or terminate of a given server"""

    @web.authenticated
    async def delete(self, name):
        """Delete a server proxy by name"""
        try:
            val = await manager.terminate_server_proxy_app(name)
            if val is None:
                raise Exception(
                    f"Proxy {name} not found. Are you sure the {name} "
                    f"is managed by jupyter-server-proxy?"
                )
            else:
                self.set_status(204)
                self.finish()
        except Exception as e:
            raise web.HTTPError(404, str(e))

    @web.authenticated
    async def get(self, name):
        """Get meta data of a running server proxy"""
        app = manager.get_server_proxy_app(name)
        self.set_status(200)
        self.finish(json.dumps(app._asdict()))


class ListServersAPIHandler(JupyterHandler):
    """Handler to list all running server proxies"""

    @web.authenticated
    async def get(self):
        """list running servers"""
        apps = manager.list_server_proxy_apps()
        self.set_status(200)
        self.finish(json.dumps([app._asdict() for app in apps]))
