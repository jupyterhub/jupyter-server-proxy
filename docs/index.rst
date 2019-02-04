================================================
Welcome to Jupyter Server Proxy's documentation!
================================================

Jupyter Server Proxy lets you run arbitrary external processes (such
as RStudio, Shiny Server, syncthing, PostgreSQL, etc) alongside your
notebook, and provide authenticated web access to them.

.. note::

    This project used to be called **nbserverproxy**. if you have an older
    version of nbserverproxy installed, remember to uninstall it before install
    jupyter-server-proxy - otherwise they may conflict

The primary use cases are:

#. Use with JupyterHub / Binder to allow launching users into web
   interfaces that have nothing to do with Jupyter - such as RStudio,
   Shiny, or OpenRefine.
#. Allow access from frontend javascript (in classic notebook or
   JupyterLab extensions) to access web APIs of other processes
   running locally in a safe manner. This is used by the `JupyterLab
   extension <https://github.com/dask/dask-labextension>`_ for 
   `dask <https://dask.org/>`_.


Contents
========

.. toctree::
   :maxdepth: 2

   install
   server-process
   launchers
   arbitrary-ports

Contributing
============

Contributions of all kinds - documentation, issues, blog posts, code, are most welcome!

.. toctree::
   :maxdepth: 2

   contributing/release