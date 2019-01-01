================================================
Welcome to Jupyter Server Proxy's documentation!
================================================

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

Installation
============

Jupyter Server Proxy can be installed with ``pip``. You must install

.. code:: bash

   pip install jupyter-server-proxy


If you have multiple virtualenvs or conda environments, you
must install ``jupyter-server-proxy`` into the same environment
your notebook is running from, rather than where your kernels are.

Accesssing arbitrary ports
==========================

If you already have a server running on localhost listening on
a port, you can access it through the notebook at
``<notebook-base>/proxy/<port>``.

With JupyterHub
---------------

Let's say you are using a JupyterHub set up on a remote machine,
and you have a process running on that machine listening on port
8080. If your hub URL is ``myhub.org``, each user can
access the service running on port 8080 with the URL
``myhub.org/hub/user-redirect/proxy/8080``. The ``user-redirect``
will make sure that:

#. It provides a redirect to the correct URL for the particular
   user who is logged in
#. If a user is not logged in, it'll present them with a login
   screen. They'll be redirected there after completing authentication.

You can also set ``c.Spawner.default_url`` to ``/proxy/8080`` to have
users be shown to your application directly after logging in -
without ever seeing the notebook interface.

Without JupyterHub
------------------

A very similar set up works when you don't use JupyterHub. You
can construct the URL with ``<notebook-url>/proxy/<port>``.

If your notebook url is ``http://localhost:8888`` and you have
a process running listening on port 8080, you can access it with
the URL ``http://localhost:8888/proxy/8080``.

This is mostly useful for testing, since you can normally just
access services on your local machine directly.