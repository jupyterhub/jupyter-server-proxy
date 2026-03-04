"""
A simple translation layer between tornado websockets and asyncio stream
connections.

This provides similar functionality to websockify
(https://github.com/novnc/websockify) without needing an extra proxy hop
or process through with all messages pass for translation.
"""

import asyncio

from tornado import web

from .handlers import NamedLocalProxyHandler, SuperviseAndProxyHandler


class RawSocketProtocol(asyncio.Protocol):
    """
    A protocol handler for the proxied stream connection.
    Sends any received blocks directly as websocket messages.
    """

    def __init__(self, handler):
        self.handler = handler

    def data_received(self, data):
        "Send the buffer as a websocket message."
        self.handler._record_activity()
        # ignore async "semi-synchronous" result, waiting is only needed for control flow and errors
        # (see https://github.com/tornadoweb/tornado/blob/bdfc017c66817359158185561cee7878680cd841/tornado/websocket.py#L1073)
        self.handler.write_message(data, binary=True)

    def connection_lost(self, exc):
        "Close the websocket connection."
        self.handler.log.info(
            f"Raw websocket {self.handler.name} connection lost: {exc}"
        )
        self.handler.close()


class RawSocketHandler(NamedLocalProxyHandler):
    """
    HTTP handler that proxies websocket connections into a backend stream.
    All other HTTP requests return 405.
    """

    def _create_ws_connection(self, proto: asyncio.BaseProtocol):
        "Create the appropriate backend asyncio connection"
        loop = asyncio.get_running_loop()
        if self.unix_socket is not None:
            self.log.info(f"RawSocket {self.name} connecting to {self.unix_socket}")
            return loop.create_unix_connection(proto, self.unix_socket)
        else:
            self.log.info(f"RawSocket {self.name} connecting to port {self.port}")
            return loop.create_connection(proto, "localhost", self.port)

    async def proxy(self, port, path):
        raise web.HTTPError(
            405, "this raw_socket_proxy backend only supports websocket connections"
        )

    async def proxy_open(self, host, port, proxied_path=""):
        """
        Open the backend connection. host and port are ignored (as they are in
        the parent for unix sockets) since they are always passed known values.
        """
        transp, proto = await self._create_ws_connection(
            lambda: RawSocketProtocol(self)
        )
        self.ws_transp = transp
        self.ws_proto = proto
        self._record_activity()
        self.log.info(f"RawSocket {self.name} connected")

        # Start periodic websocket keepalive pings to avoid idle timeout by intermediates.
        # Browser will respond with pong automatically, which counts as activity on many proxies.
        try:
            self._keepalive_task = asyncio.create_task(self._ws_keepalive())
        except Exception as exc:
            # If scheduling keepalive fails, log but continue; data traffic will still keep connection alive.
            self.log.warning(
                f"RawSocket {self.name} failed to start keepalive task: {exc}"
            )

    def on_message(self, message):
        "Send websocket messages as stream writes, encoding if necessary."
        self._record_activity()
        if isinstance(message, str):
            message = message.encode("utf-8")
        self.ws_transp.write(
            message
        )  # buffered non-blocking. should block (needs new enough tornado)

    def on_ping(self, message):
        "No-op"
        self._record_activity()

    async def _ws_keepalive(self):
        """
        Periodically send websocket ping frames to keep the connection alive.
        Many reverse proxies/load balancers close idle websockets (~60s) without traffic.
        """
        # Default to 30s; adjust if your environment has stricter idle policies.
        interval_seconds = 30
        try:
            while True:
                await asyncio.sleep(interval_seconds)
                # Send a small ping payload; browsers reply with pong automatically.
                self._record_activity()
                try:
                    self.ping(b"keepalive")
                except Exception as exc:
                    # If ping fails (connection closed), exit loop.
                    self.log.debug(
                        f"RawSocket {self.name} keepalive ping failed: {exc}"
                    )
                    break
        except asyncio.CancelledError:
            # Task cancelled during handler close; swallow exception.
            pass

    def on_close(self):
        "Close the backend connection."
        self.log.info(f"RawSocket {self.name} connection closed")
        # Stop keepalive task if running
        if hasattr(self, "_keepalive_task") and self._keepalive_task:
            try:
                self._keepalive_task.cancel()
            except Exception:
                pass
        if hasattr(self, "ws_transp"):
            self.ws_transp.close()


class SuperviseAndRawSocketHandler(SuperviseAndProxyHandler, RawSocketHandler):
    async def _http_ready_func(self, p):
        # not really HTTP here, just try an empty connection
        try:
            transp, _ = await self._create_ws_connection(asyncio.Protocol)
        except OSError as exc:
            self.log.debug(f"RawSocket {self.name} connection check failed: {exc}")
            return False
        transp.close()
        return True
