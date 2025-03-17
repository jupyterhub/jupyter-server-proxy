"""
Test whether ServerProcessEntryPoint can be configured using traitlets
"""

import sys
from pathlib import Path

from traitlets.config import default

from jupyter_server_proxy import ServerProcessEntryPoint


class CustomServerProcessEntryPoint(ServerProcessEntryPoint):
    @default("command")
    def _default_command(self):
        parent = Path(__file__).parent.resolve()
        return [sys.executable, str(parent / "httpinfo.py"), "--port={port}"]
