import socket

from tornado.netutil import Resolver


class UnixResolver(Resolver):
    def initialize(self, socket_path):
        self.socket_path = socket_path

    async def resolve(self, host, port, *args, **kwargs):
        return [(socket.AF_UNIX, self.socket_path)]
