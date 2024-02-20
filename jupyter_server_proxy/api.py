import mimetypes

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
                    "category": sp.launcher_entry.category,
                },
                "new_browser_tab": sp.new_browser_tab,
            }
            if sp.launcher_entry.icon_path:
                icon_url = ujoin(self.base_url, "server-proxy", "icon", sp.name)
                item["launcher_entry"]["icon_url"] = icon_url

            data.append(item)

        self.write({"server_processes": data})


# FIXME: Should be a StaticFileHandler subclass
class IconHandler(JupyterHandler):
    """
    Serve launcher icons
    """

    def initialize(self, icons):
        """
        icons is a dict of titles to paths
        """
        self.icons = icons

    async def get(self, name):
        if name not in self.icons:
            raise web.HTTPError(404)
        path = self.icons[name]

        # Guess mimetype appropriately
        # Stolen from https://github.com/tornadoweb/tornado/blob/b399a9d19c45951e4561e6e580d7e8cf396ef9ff/tornado/web.py#L2881
        mime_type, encoding = mimetypes.guess_type(path)
        if encoding == "gzip":
            content_type = "application/gzip"
        # As of 2015-07-21 there is no bzip2 encoding defined at
        # http://www.iana.org/assignments/media-types/media-types.xhtml
        # So for that (and any other encoding), use octet-stream.
        elif encoding is not None:
            content_type = "application/octet-stream"
        elif mime_type is not None:
            content_type = mime_type
        # if mime_type not detected, use application/octet-stream
        else:
            content_type = "application/octet-stream"

        with open(self.icons[name]) as f:
            self.write(f.read())
        self.set_header("Content-Type", content_type)
