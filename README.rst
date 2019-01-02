====================
Jupyter Server Proxy
====================

Jupyter Server Proxy lets you run arbitrary external processes (such
as RStudio, Shiny Server, syncthing, PostgreSQL, etc) alongside your
notebook, and provide authenticated web access to them.

The primary use cases are:

#. Use with JupyterHub / Binder to allow launching users into web
   interfaces that have nothing to do with Jupyter - such as RStudio,
   Shiny, or OpenRefine.
#. Allow access from frontend javascript (in classic notebook or
   JupyterLab extensions) to access web APIs of other processes
   running locally in a safe manner. This is used by the `JupyterLab
   extension <https://github.com/dask/dask-labextension>`_ for 
   `dask <https://dask.org/>`_.


`The documentation <https://jupyter-server-proxy.readthedocs.io/>`_
contains information on installation & usage.