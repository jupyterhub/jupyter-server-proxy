.. _contributing/release:

================
Making a release
================

We should release early & often, following `semver <https://semver.org/>`_ wherever possible.

Packages in this repository
===========================

This repo has more than one package.

#. The primary ``jupyter-server-proxy`` python package. This contains the actual
   proxying code, and the classic notebook extension. This is published on `PyPI
   <https://pypi.org/project/jupyter-server-proxy>`_.

#. The JupyterLab plugin, ``jupyterlab-server-proxy``. This provides the
   launcher icons in JupyterLab. This is packaged into the Python package but
   also published to `NPM
   <https://www.npmjs.com/package/@jupyterlab/server-proxy>`_ for JupyterLab 2
   compatibility.

#. Various python packages in ``contrib/``. These are convenience packages that
   help set up a particular application for use - such as Theia.

As of version 3.0.0, we keep the version numbers of the main Python package and
the JupyterLab plugin in sync, but have no procedure for the Theia package yet.
NPM package versioning is stricter than Python package versioning.
For example if you want to release a release candidate the version should be in the form `3.0.0-rc.1`, python will automatically treat this as `3.0.0rc1`.

Gaining Access Privileges
=========================

To make a release, you only need privileges to create a tag as there is
automation to publish in GitHub workflows when a tag is pushed.

Release checklist
=================

#. Update the package version number in
   ``jupyterlab-server-proxy/package.json``, it will be read by ``setup.py``.

#. Commit these changes and make a pull request with it. 

#. Once pull request is merged, make a tag of form ``v<version-number>``:

   .. code::

      git tag -a v<version-number>

   And push it to the official repository

   .. code::
     
      git push git@github.com:jupyterhub/jupyter-server-proxy --tags
