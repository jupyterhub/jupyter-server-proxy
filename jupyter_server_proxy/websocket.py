"""
Authenticated HTTP proxy for Jupyter Notebooks

Some original inspiration from https://github.com/senko/tornado-proxy
"""

import inspect

from jupyter_server.utils import ensure_async
from tornado import httpclient, httputil, websocket


class PingableWSClientConnection(websocket.WebSocketClientConnection):
    """A WebSocketClientConnection with an on_ping callback."""

    def __init__(self, **kwargs):
        if "on_ping_callback" in kwargs:
            self._on_ping_callback = kwargs["on_ping_callback"]
            del kwargs["on_ping_callback"]
        super().__init__(**kwargs)

    def on_ping(self, data):
        if self._on_ping_callback:
            self._on_ping_callback(data)


def pingable_ws_connect(
    request=None,
    on_message_callback=None,
    on_ping_callback=None,
    subprotocols=None,
    resolver=None,
):
    """
    A variation on websocket_connect that returns a PingableWSClientConnection
    with on_ping_callback.
    """
    # Copy and convert the headers dict/object (see comments in
    # AsyncHTTPClient.fetch)
    request.headers = httputil.HTTPHeaders(request.headers)
    request = httpclient._RequestProxy(request, httpclient.HTTPRequest._DEFAULTS)

    # resolver= parameter requires tornado >= 6.3. Only pass it if needed
    # (for Unix socket support), so older versions of tornado can still
    # work otherwise.
    kwargs = {"resolver": resolver} if resolver else {}
    conn = PingableWSClientConnection(
        request=request,
        compression_options={},
        on_message_callback=on_message_callback,
        on_ping_callback=on_ping_callback,
        max_message_size=getattr(
            websocket, "_default_max_message_size", 10 * 1024 * 1024
        ),
        subprotocols=subprotocols,
        **kwargs,
    )

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
            raise Exception(
                "WebSocketHandlerMixin should be followed "
                "by another parent to make sense"
            )

        # undisallow methods --- t.ws.WebSocketHandler disallows methods,
        # we need to re-enable these methods
        def wrapper(method):
            def undisallow(*args2, **kwargs2):
                getattr(nextparent, method)(self, *args2, **kwargs2)

            return undisallow

        for method in [
            "write",
            "redirect",
            "set_header",
            "set_cookie",
            "set_status",
            "flush",
            "finish",
        ]:
            setattr(self, method, wrapper(method))
        nextparent.__init__(self, *args, **kwargs)

    async def get(self, *args, **kwargs):
        if self.request.headers.get("Upgrade", "").lower() != "websocket":
            return await self.http_get(*args, **kwargs)
        else:
            await ensure_async(super().get(*args, **kwargs))
