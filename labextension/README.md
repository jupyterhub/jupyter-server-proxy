# `@jupyterhub/jupyter-server-proxy`

A pre-built JupyterLab extension that adds items to the JupyterLab [Launcher]
to open server processes managed by the python package
[`jupyter-server-proxy`](https://pypi.org/project/jupyter-server-proxy).

[launcher]: https://jupyterlab.readthedocs.io/en/stable/extension/extension_points.html#launcher

## Prerequisites

- JupyterLab >=3,<5

## Installation

Use your preferred Python package manager to install `jupyter-server-proxy`:

```bash
pip install jupyter-server-proxy
```

or

```bash
conda install -c conda-forge jupyter-server-proxy
```

> As a _prebuilt_ extension, it will "just work," only a simple page reload should be required
> to see launcher items. However, a full restart of `jupyter_server` or `notebook` is required
> to reload the `jupyter_server_proxy` serverextension which provides most of the functionality.

For a full development and testing installation, see the
[contributing guide](https://github.com/jupyterhub/jupyter-server-proxy/blob/main/CONTRIBUTING.md).
