====================
Jupyter Server Proxy
====================

|ReadTheDocs badge| |Travis badge| |PyPI badge| |Conda badge| |NPM badge|

.. |ReadTheDocs badge| image:: https://img.shields.io/readthedocs/jupyter-server-proxy?logo=read-the-docs
   :target: https://jupyter-server-proxy.readthedocs.io/

.. |Travis badge| image:: https://img.shields.io/travis/com/jupyterhub/jupyter-server-proxy?logo=travis
   :target: https://travis-ci.com/jupyterhub/jupyter-server-proxy

.. |PyPI badge| image:: https://img.shields.io/pypi/v/jupyter-server-proxy.svg?logo=pypi
   :target: https://pypi.python.org/pypi/jupyter-server-proxy

.. |Conda badge| image:: https://img.shields.io/conda/vn/conda-forge/jupyter-server-proxy?logo=conda-forge
   :target: https://anaconda.org/conda-forge/jupyter-server-proxy

.. |NPM badge| image:: https://img.shields.io/npm/v/@jupyterlab/server-proxy.svg?logo=npm
   :target: https://www.npmjs.com/package/@jupyterlab/server-proxy

Jupyter Server Proxy lets you run arbitrary external processes (such
as RStudio, Shiny Server, Syncthing, PostgreSQL, Code Server, etc)
alongside your notebook server and provide authenticated web access to
them using a path like ``/rstudio`` next to others like ``/lab``.
Alongside the python package that provides the main functionality, the
JupyterLab extension (``@jupyterlab/server-proxy``) provides buttons
in the JupyterLab launcher window to get to RStudio for example.

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

Install
=======

Python package
--------------

pip
^^^

.. code-block::

   pip install jupyter-server-proxy

conda
^^^^^

.. code-block::

   conda install jupyter-server-proxy -c conda-forge

JupyterLab extension
--------------------

Note that as the JupyterLab extension only is a graphical interface to
launch registered applications in the python package, the extension
requires the python package to be installed.

.. code-block::

   jupyter labextension install @jupyterlab/server-proxy

Contributing
============

Python package
--------------

.. code-block::

   pip install -e .

   # explicit install needed with editable mode (-e) jupyter
   jupyter serverextension enable --sys-prefix jupyter_server_proxy


JupyterLab extension
--------------------

The ``jlpm`` command is JupyterLab's pinned version of ``yarn`` that
is installed with JupyterLab. You may use ``yarn`` or ``npm`` instead
of ``jlpm`` below.

.. code-block::

   cd jupyterlab-server-proxy
   # Install dependencies
   jlpm
   # Build Typescript source
   jlpm build
   # Link your development version of the extension with JupyterLab
   jupyter labextension link .
   # Rebuild Typescript source after making changes
   jlpm build
   # Rebuild JupyterLab after making any changes
   jupyter lab build

You can watch the source directory and run JupyterLab in watch mode to
watch for changes in the extension's source and automatically rebuild
the extension and application.

.. code-block::

   # Watch the source directory in another terminal tab
   jlpm watch
   # Run jupyterlab in watch mode in one terminal tab
   jupyter lab --watch
