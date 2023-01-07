# `@jupyterhub/jupyter-server-proxy`

A JupyterLab extension that adds items to the JupyterLab [Launcher] representing the
configured server processes managed by the python package `jupyter-server-proxy` (required).

[launcher]: https://jupyterlab.readthedocs.io/en/stable/extension/extension_points.html#launcher

## Prerequisites

- JupyterLab >=2,<4

## Installation

For JupyterLab 3, use your preferred Python package manager to install `jupyter-server-proxy`:

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

### JupyterLab 2

For JupyterLab 2, ensure `nodejs` is installed and available on `$PATH` and run:

```bash
jupyter labextension install @jupyterhub/jupyter-server-proxy
```

> This will cause:
>
> - a download of a great deal of build assets from `npmjs.org`
> - a large `webpack` build that may exhaust memory and open files handles
>
> **Please** consider upgrading to JupyterLab 3 before reporting issues.
