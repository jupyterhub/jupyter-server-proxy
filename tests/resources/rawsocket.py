#!/usr/bin/env python

import socket
import sys

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} TCPPORT|SOCKPATH")
    sys.exit(1)
where = sys.argv[1]
try:
    port = int(where)
    family = socket.AF_INET
    addr = ("localhost", port)
except ValueError:
    family = socket.AF_UNIX
    addr = where

with socket.create_server(addr, family=family) as serv:
    while True:
        # only handle a single connection at a time
        sock, caddr = serv.accept()
        while True:
            s = sock.recv(1024)
            if not s:
                break
            sock.send(s.swapcase())
        sock.close()
