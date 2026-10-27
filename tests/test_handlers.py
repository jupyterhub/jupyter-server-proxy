from unittest import mock

from tornado.websocket import WebSocketClosedError

from jupyter_server_proxy import handlers


def _fake_handler():
    handler = mock.Mock()
    handler._check_host_allowlist.return_value = True
    handler.unix_socket = None
    handler.get_client_uri.return_value = "ws://localhost:8080/"
    handler.proxy_request_headers.return_value = {}
    handler._requested_subprotocols = None
    handler.selected_subprotocol = None
    return handler


async def test_backend_message_after_client_closed(monkeypatch):
    callbacks = {}

    async def fake_connect(request, on_message_callback, **kwargs):
        callbacks["message"] = on_message_callback
        return mock.Mock(selected_subprotocol=None)

    monkeypatch.setattr(handlers, "pingable_ws_connect", fake_connect)
    handler = _fake_handler()
    await handlers.ProxyHandler.proxy_open(handler, "localhost", 8080, "/")

    handler.write_message.side_effect = WebSocketClosedError()
    callbacks["message"]("goodbye")
    handler.close.assert_called_once_with()


def test_client_message_after_backend_closed():
    handler = _fake_handler()
    handler.ws.write_message.side_effect = WebSocketClosedError()
    handlers.ProxyHandler.on_message(handler, "hello")
    handler.close.assert_called_once_with()
