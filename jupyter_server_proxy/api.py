import json

from jupyter_server.base.handlers import JupyterHandler
from jupyter_server.utils import url_path_join as ujoin
from tornado import web


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


# IconHandler has been copied from JupyterHub's IconHandler:
# https://github.com/jupyterhub/jupyterhub/blob/4.0.0b2/jupyterhub/handlers/static.py#L22-L31
class ServersIconHandler(web.StaticFileHandler):
    """A singular handler for serving the icon."""

    def get(self):
        return super().get("")

    @classmethod
    def get_absolute_path(cls, root, path):
        """We only serve one file, ignore relative path"""
        import os

        return os.path.abspath(root)


class ServersAPIHandler(JupyterHandler):
    """Handler to get metadata or terminate of a given server or all servers"""

    def initialize(self, manager):
        self.manager = manager

    @web.authenticated
    async def delete(self, name):
        """Delete a server proxy by name"""
        if not name:
            raise web.HTTPError(
                403,
                "Please set the name of a running server proxy that "
                "user wishes to terminate",
            )

        try:
            val = await self.manager.terminate_server_proxy_app(name)
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
        if name:
            apps = self.manager.get_server_proxy_app(name)._asdict()
            # If no server proxy found this will be a dict with empty values
            if not apps["name"]:
                raise web.HTTPError(404, f"Server proxy {name} not found")
        else:
            apps = [app._asdict() for app in self.manager.list_server_proxy_apps()]

        self.set_status(200)
        self.finish(json.dumps(apps))


def setup_api_handlers(web_app, manager, server_processes):
    base_url = web_app.settings["base_url"]

    # Make a list of icon handlers
    icon_handlers = []
    for sp in server_processes:
        if sp.launcher_entry.enabled and sp.launcher_entry.icon_path:
            icon_handlers.append(
                (
                    ujoin(base_url, f"server-proxy/icon/{sp.name}"),
                    ServersIconHandler,
                    {"path": sp.launcher_entry.icon_path},
                )
            )

    web_app.add_handlers(
        ".*",
        [
            (
                ujoin(base_url, "server-proxy/api/servers-info"),
                ServersInfoHandler,
                {"server_processes": server_processes},
            ),
            (
                ujoin(base_url, r"server-proxy/api/servers/(?P<name>.*)"),
                ServersAPIHandler,
                {"manager": manager},
            ),
        ]
        + icon_handlers,
    )
