#!/usr/bin/env python
#
# Based on the chat demo from https://github.com/tornadoweb/tornado/blob/d6819307ee050bbd8ec5deb623e9150ce2220ef9/demos/websocket/chatdemo.py#L1
# Original License:
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


import json
import os.path

import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/echosocket", EchoWebSocket),
            (r"/subprotocolsocket", SubprotocolWebSocket),
            (r"/headerssocket", HeadersWebSocket),
        ]
        settings = dict(
            cookie_secret="__RANDOM_VALUE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
        )
        super().__init__(handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world!")


class EchoWebSocket(tornado.websocket.WebSocketHandler):
    """Echoes back received messages."""

    def on_message(self, message):
        self.write_message(message)


class HeadersWebSocket(tornado.websocket.WebSocketHandler):
    """Echoes back incoming request headers."""

    def on_message(self, message):
        self.write_message(json.dumps(dict(self.request.headers)))


class SubprotocolWebSocket(tornado.websocket.WebSocketHandler):
    """
    Echoes back requested subprotocols and selected subprotocol as a JSON
    encoded message, and selects subprotocols in a very particular way to help
    us test things.
    """

    def __init__(self, *args, **kwargs):
        self._requested_subprotocols = None
        super().__init__(*args, **kwargs)

    def select_subprotocol(self, subprotocols):
        self._requested_subprotocols = subprotocols if subprotocols else None

        if not subprotocols:
            return None
        if "please_select_no_protocol" in subprotocols:
            return None
        if "favored" in subprotocols:
            return "favored"
        else:
            return subprotocols[0]

    def on_message(self, message):
        response = {
            "requested_subprotocols": self._requested_subprotocols,
            "selected_subprotocol": self.selected_subprotocol,
        }
        self.write_message(json.dumps(response))


def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
