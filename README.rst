====================
Jupyter Server Proxy
====================

|ReadTheDocs badge| |Travis badge| |PyPI badge| |Conda badge| |NPM badge|

.. |ReadTheDocs badge| image:: https://img.shields.io/readthedocs/jupyter-server-proxy?logo=read-the-docs
   :target: https://jupyter-server-proxy.readthedocs.io/

.. |Travis badge| image:: https://img.shields.io/travis/jupyterhub/jupyter-server-proxy/master.svg?logo=travis
   :target: https://travis-ci.org/jupyterhub/jupyter-server-proxy

.. |PyPI badge| image:: https://img.shields.io/pypi/v/jupyter-server-proxy.svg?logo=pypi
   :target: https://pypi.python.org/pypi/jupyter-server-proxy

.. |Conda badge| image:: https://img.shields.io/conda/vn/conda-forge/jupyter-server-proxy?logo=conda-forge
   :target: https://anaconda.org/conda-forge/jupyter-server-proxy

.. |NPM badge| image:: https://img.shields.io/npm/v/jupyterlab-server-proxy.svg?logo=npm
   :target: https://www.npmjs.com/package/jupyterlab-server-proxy

Jupyter Server Proxy lets you run arbitrary external processes (such
as RStudio, Shiny Server, syncthing, PostgreSQL, etc) alongside your
notebook, and provide authenticated web access to them.

**Note:** This project used to be called **nbserverproxy**. As
nbserverproxy is an older version of jupyter-server-proxy, uninstall
nbserverproxy before installing jupyter-server-proxy to avoid
conflicts.

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
