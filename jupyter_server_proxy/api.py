from tornado import web
import mimetypes
from jupyter_server.base.handlers import JupyterHandler
from jupyter_server.utils import url_path_join as ujoin
from collections import namedtuple

class ServersInfoHandler(JupyterHandler):
    def initialize(self, server_processes):
        self.server_processes = server_processes

    @web.authenticated
    async def get(self):
        data = []
        # Pick out and send only metadata
        # Don't send anything that might be a callable, or leak sensitive info
        for sp in self.server_processes:
            item = {
                'name': sp.name,
                'launcher_entries': []
            }

            for le in sp.launcher_entries:
                litem = {
                    'enabled': le.enabled,
                    'title': le.title,
                    'new_browser_tab': le.new_browser_tab,
                    'path': le.path
                }

                # Manually recurse to convert namedtuples into JSONable structures
                if le.icon_path:
                    icon_url = ujoin(self.base_url, 'server-proxy', 'icon', sp.name, le.name)
                    litem['icon_url'] = icon_url

                item['launcher_entries'].append(litem)

            data.append(item)

        self.write({'server_processes': data})


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
        name = tuple(name.split("/", 1))
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

        with open(self.icons[name], "rb") as f:
            self.write(f.read())
        self.set_header('Content-Type', content_type)
