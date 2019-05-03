from jupyter_server_proxy.handlers import ProxyHandler
from notebook.utils import url_path_join

class NewHandler(ProxyHandler):
    async def http_get(self):
        return await self.proxy()

    async def open(self):
        host = '127.0.0.1'
        port = 54321
        return await super().proxy_open(host, port)

    def post(self):
        return self.proxy()

    def put(self):
        return self.proxy()

    def delete(self):
        return self.proxy()

    def head(self):
        return self.proxy()

    def patch(self):
        return self.proxy()

    def options(self):
        return self.proxy()

    def proxy(self):
        host = '127.0.0.1'
        port = 54321
        proxied_path = ''
        return super().proxy(host, port, proxied_path)


def _jupyter_server_extension_paths():
    return [{"module": "dask_labextension"}]


def load_jupyter_server_extension(nb_server_app):
    web_app = nb_server_app.web_app
    base_url = web_app.settings["base_url"]
    proxy_path = url_path_join(base_url, "newproxy/" + "?")
    handlers = [(proxy_path, NewHandler)]
    web_app.add_handlers(".*$", handlers)
