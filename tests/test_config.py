import logging
from traitlets.config import Config

from jupyter_server_proxy.config import ServerProxy


def test_deprecated_config(caplog):
    cfg = Config()
    cfg.ServerProxy.host_whitelist = ['jupyter.example.org']
    log = logging.getLogger("testlog")
    server_proxy = ServerProxy(config=cfg, log=log)
    assert caplog.record_tuples == [
        (
            log.name,
            logging.WARNING,
            'ServerProxy.host_whitelist is deprecated in jupyter-server-proxy 3.0.0, use ServerProxy.host_allowlist instead',
        )
    ]
    assert server_proxy.host_allowlist == ['jupyter.example.org']
