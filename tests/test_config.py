import pytest
from traitlets.config import Config

from jupyter_server_proxy.config import ServerProxy


def test_deprecated_config():
    expected = "ServerProxy.host_whitelist is deprecated in jupyter-server-proxy 3.0.0, use ServerProxy.host_allowlist instead"
    cfg = Config()
    cfg.ServerProxy.host_whitelist = ["jupyter.example.org"]
    with pytest.warns(UserWarning, match=expected):
        server_proxy = ServerProxy(config=cfg)
    assert server_proxy.host_allowlist == ["jupyter.example.org"]
