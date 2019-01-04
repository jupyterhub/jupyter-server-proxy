=================================
User Contributed Server Processes
=================================

This directory contains various python packages that can be
pip installed to get popular services that are commonly
used with jupyter-server-proxy working.

Making a new package
====================

There is a `cookiecutter <https://github.com/audreyr/cookiecutter>`_
template provided here that can be used to make new packages.

.. code:: bash

   pip install cookiecutter
   cookiecutter template

This should ask you a bunch of questions, and generate a directory
named after your project with a python package. From there, you should:

#. Edit the ``__init__.py`` file to fill in the command used to start your
   process, any environment variables, and title of the launcher icon

#. (Optionally) Add a square svg icon for your launcher in the ``icons``
   subfolder, with the same name as your project.