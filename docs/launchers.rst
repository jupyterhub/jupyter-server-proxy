.. _launchers:

=============
GUI Launchers
=============

Jupyter Server Proxy automatically adds entries for :ref:`registered
Server Processes <server-process>` in both the classic Jupyter Notebook
interface and the JupyterLab Launcher.

Classic Notebook Extension
==========================

By default, an entry is made for each server process under the 'New'
menu in the notebook's default tree view. Note that a new instance
is **not** launched every time you click an item - if the process
is already running, it is reused.

.. image:: images/nbextension-tree.png

JupyterLab Launcher Extension
=============================

The jupyterlab-server-proxy JupyterLab extension can be installed
to provide launcher icons for registered server processes.

.. code:: bash

   jupyter labextension install @jupyterlab/server-proxy

This should provide icons for each registered process in the main
JupyterLab launcher

.. image:: images/labextension-launcher.png

Clicking on them will open the application in a new window.
