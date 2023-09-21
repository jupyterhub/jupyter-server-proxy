# `@jupyterhub/jupyter-server-proxy`

A JupyterLab extension that adds items to the JupyterLab [Launcher] representing the
configured server processes managed by the python package `jupyter-server-proxy` (required).

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
conda install jupyter-server-proxy
```

> As a _prebuilt_ extension, it will "just work," only a simple page reload should be required
> to see launcher items. However, a full restart of `jupyter_server` or `notebook` is required
> to reload the `jupyter_server_proxy` serverextension which provides most of the functionality.
