"""
Authenticated HTTP proxy for Jupyter Notebooks

Some original inspiration from https://github.com/senko/tornado-proxy
"""

import inspect
import socket
import os
from urllib.parse import urlunparse, urlparse

from tornado import gen, web, httpclient, httputil, process, websocket, ioloop, version_info

from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler, utcnow

try:
    # Tornado 6.0 deprecated its `maybe_future` function so `notebook` made their own.
    # See: https://github.com/jupyter/notebook/pull/4453
    from notebook.utils import maybe_future
except ImportError:
    # We can't find it in `notebook` then we should be able to find it in Tornado
    from tornado.gen import maybe_future


class PingableWSClientConnection(websocket.WebSocketClientConnection):
    """A WebSocketClientConnection with an on_ping callback."""
    def __init__(self, **kwargs):
        if 'on_ping_callback' in kwargs:
            self._on_ping_callback = kwargs['on_ping_callback']
            del(kwargs['on_ping_callback'])
        super().__init__(**kwargs)

    def on_ping(self, data):
        if self._on_ping_callback:
            self._on_ping_callback(data)


def pingable_ws_connect(request=None,on_message_callback=None,
                        on_ping_callback=None, subprotocols=None):
    """
    A variation on websocket_connect that returns a PingableWSClientConnection
    with on_ping_callback.
    """
    # Copy and convert the headers dict/object (see comments in
    # AsyncHTTPClient.fetch)
    request.headers = httputil.HTTPHeaders(request.headers)
    request = httpclient._RequestProxy(
        request, httpclient.HTTPRequest._DEFAULTS)

    # for tornado 4.5.x compatibility
    if version_info[0] == 4:
        conn = PingableWSClientConnection(io_loop=ioloop.IOLoop.current(),
            compression_options={},
            request=request,
            on_message_callback=on_message_callback,
            on_ping_callback=on_ping_callback)
    else:
        conn = PingableWSClientConnection(request=request,
            compression_options={},
            on_message_callback=on_message_callback,
            on_ping_callback=on_ping_callback,
            max_message_size=getattr(websocket, '_default_max_message_size', 10 * 1024 * 1024),
            subprotocols=subprotocols)

    return conn.connect_future

# from https://stackoverflow.com/questions/38663666/how-can-i-serve-a-http-page-and-a-websocket-on-the-same-url-in-tornado
class WebSocketHandlerMixin(websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # since my parent doesn't keep calling the super() constructor,
        # I need to do it myself
        bases = inspect.getmro(type(self))
        assert WebSocketHandlerMixin in bases
        meindex = bases.index(WebSocketHandlerMixin)
        try:
            nextparent = bases[meindex + 1]
        except IndexError:
            raise Exception("WebSocketHandlerMixin should be followed "
                            "by another parent to make sense")

        # undisallow methods --- t.ws.WebSocketHandler disallows methods,
        # we need to re-enable these methods
        def wrapper(method):
            def undisallow(*args2, **kwargs2):
                getattr(nextparent, method)(self, *args2, **kwargs2)
            return undisallow

        for method in ["write", "redirect", "set_header", "set_cookie",
                       "set_status", "flush", "finish"]:
            setattr(self, method, wrapper(method))
        nextparent.__init__(self, *args, **kwargs)

    async def get(self, *args, **kwargs):
        if self.request.headers.get("Upgrade", "").lower() != 'websocket':
            return await self.http_get(*args, **kwargs)
        else:
            await maybe_future(super().get(*args, **kwargs))


def setup_handlers(web_app):
    host_pattern = '.*$'
    web_app.add_handlers('.*', [
        (url_path_join(web_app.settings['base_url'], r'/proxy/(\d+)(.*)'), LocalProxyHandler)
    ])

# vim: set et ts=4 sw=4:
