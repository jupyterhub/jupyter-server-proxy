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


import logging
import json
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path
import uuid

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/echosocket", EchoWebSocket),
            (r"/subprotocolsocket", SubprotocolWebSocket),
        ]
        settings = dict(
            cookie_secret="__RANDOM_VALUE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
        )
        super(Application, self).__init__(handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world!")


class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def on_message(self, message):
        self.write_message(message)


class SubprotocolWebSocket(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        self._subprotocols = None
        super().__init__(*args, **kwargs)

    def select_subprotocol(self, subprotocols):
        self._subprotocols = subprotocols
        return None

    def on_message(self, message):
        self.write_message(json.dumps(self._subprotocols))


def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
