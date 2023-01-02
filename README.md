# Jupyter Server Proxy

[![ReadTheDocs badge](https://img.shields.io/readthedocs/jupyter-server-proxy?logo=read-the-docs)](https://jupyter-server-proxy.readthedocs.io/)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/jupyterhub/jupyter-server-proxy/Test?logo=github)](https://github.com/jupyterhub/jupyter-server-proxy/actions)
[![PyPI badge](https://img.shields.io/pypi/v/jupyter-server-proxy.svg?logo=pypi)](https://pypi.python.org/pypi/jupyter-server-proxy)
[![Conda badge](https://img.shields.io/conda/vn/conda-forge/jupyter-server-proxy?logo=conda-forge)](https://anaconda.org/conda-forge/jupyter-server-proxy)
[![NPM badge](https://img.shields.io/npm/v/@jupyterhub/jupyter-server-proxy.svg?logo=npm)](https://www.npmjs.com/package/@jupyterhub/jupyter-server-proxy)

Jupyter Server Proxy lets you run arbitrary external processes (such as
RStudio, Shiny Server, Syncthing, PostgreSQL, Code Server, etc)
alongside your notebook server and provide authenticated web access to
them using a path like `/rstudio` next to others like `/lab`. Alongside
the python package that provides the main functionality, the JupyterLab
extension (`@jupyterhub/jupyter-server-proxy`) provides buttons in the
JupyterLab launcher window to get to RStudio for example.

**Note:** This project used to be called **nbserverproxy**. As
nbserverproxy is an older version of jupyter-server-proxy, uninstall
nbserverproxy before installing jupyter-server-proxy to avoid conflicts.

The primary use cases are:

1.  Use with JupyterHub / Binder to allow launching users into web
    interfaces that have nothing to do with Jupyter - such as RStudio,
    Shiny, or OpenRefine.
2.  Allow access from frontend javascript (in classic notebook or
    JupyterLab extensions) to access web APIs of other processes running
    locally in a safe manner. This is used by the [JupyterLab
    extension](https://github.com/dask/dask-labextension) for
    [dask](https://www.dask.org/).

[The documentation](https://jupyter-server-proxy.readthedocs.io/)
contains information on installation & usage.

## Security warning

Jupyter Server Proxy is often used to start a user defined process listening to
some network port (e.g. http://localhost:4567) for a user starting a Jupyter Server
that only that user has permission to access. The user can then access the
started process proxied through the Jupyter Server.

For safe use of Jupyter Server Proxy, you should ensure that the process started
by Jupyter Server proxy can't be accessed directly by another user and bypass
the Jupyter Server's authorization!

A common strategy to enforce access proxied via Jupyter Server is to start
Jupyter Server within a container and only allow network access to the Jupyter
Server via the container.

For more insights, see [Ryan Lovetts comment about
it](https://github.com/jupyterhub/jupyter-server-proxy/pull/359#issuecomment-1350118197).

## Install

### Requirements

* `jupyterlab>=2` or `notebook`

### Python package

#### pip

```bash
pip install jupyter-server-proxy
```

#### conda

```bash
conda install jupyter-server-proxy -c conda-forge
```

### JupyterLab extension

Note that as the JupyterLab extension only is a graphical interface to
launch registered applications in the python package, the extension
requires the python package to be installed.

As of version 3.0.0 the Python package ships with a JupyterLab 3 compatible
extension, making this step only needed for JupyterLab 2.

<details>
<summary>See JupyterLab 2-only steps</summary>
<pre>
jupyter labextension install @jupyterhub/jupyter-server-proxy
</pre>
</details>

## Disable

### Server extension

```bash
jupyter serverextension disable jupyter_server_proxy
```

### Notebook classic extension

```bash
jupyter nbextension disable --py jupyter_server_proxy
```

### JupyterLab extension

```bash
jupyter labextension disable @jupyterhub/jupyter-server-proxy
```

## Local development

See [CONTRIBUTING.md](CONTRIBUTING.md).
