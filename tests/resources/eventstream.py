import asyncio

import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from tornado.options import define, options


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/stream/(\d+)", StreamHandler),
        ]
        super().__init__(handlers)


class StreamHandler(tornado.web.RequestHandler):
    async def get(self, seconds):
        for i in range(int(seconds)):
            await asyncio.sleep(0.5)
            self.write(f"data: {i}\n\n")
            await self.flush()


def main():
    define("port", default=8888, help="run on the given port", type=int)
    options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
