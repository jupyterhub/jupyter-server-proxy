====================
Jupyter Server Proxy
====================

|Travis badge| |PyPI badge| |NPM badge|

.. |Travis badge| image:: https://img.shields.io/travis/jupyterhub/jupyter-server-proxy/master.svg?logo=travis
   :target: https://travis-ci.org/jupyterhub/jupyter-server-proxy

.. |PyPI badge| image:: https://img.shields.io/pypi/v/jupyter-server-proxy.svg?logo=pypi
   :target: https://pypi.python.org/pypi/jupyter-server-proxy

.. |NPM badge| image:: https://img.shields.io/npm/v/jupyterlab-server-proxy.svg?logo=npm
   :target: https://www.npmjs.com/package/jupyterlab-server-proxy

Jupyter Server Proxy lets you run arbitrary external processes (such
as RStudio, Shiny Server, syncthing, PostgreSQL, etc) alongside your
notebook, and provide authenticated web access to them.

**Note:** This project used to be called **nbserverproxy**. if you have an older
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


`The documentation <https://jupyter-server-proxy.readthedocs.io/>`_
contains information on installation & usage.

====================
Install
====================

pip
---

.. code-block::

   pip install jupyter-server-proxy

conda
-----

.. code-block::

   conda install jupyter-server-proxy -c conda-forge

src
---

.. code-block::

   pip install .

**Note:** if installing from source in editable mode: ``setup.py develop/pip install -e``, please explicitly install the server extensions:

.. code-block::

   jupyter serverextension enable --sys-prefix jupyter_server_proxy
