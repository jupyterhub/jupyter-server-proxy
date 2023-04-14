(install)=

# Installation

Jupyter Server Proxy can be installed with `pip`. You must install

```bash
pip install jupyter-server-proxy
```

If using `pip install -e` please install the server extension explicitly:

```bash
jupyter serverextension enable --sys-prefix jupyter_server_proxy
```

If you have multiple virtualenvs or conda environments, you
must install `jupyter-server-proxy` into the same environment
your notebook is running from, rather than where your kernels are.
