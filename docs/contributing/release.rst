.. _contributing/release:

================
Making a release
================

We should release early & often, following `semver <https://semver.org/>`_ wherever possible.

Packages in this repository
===========================

This repo has more than one package.

#. The primary ``jupyter-server-proxy`` python package. This contains the actual proxying
   code, and the classic notebook extension. This is published on `PyPI <https://pypi.org>`_.

#. The JupyterLab plugin, ``jupyterlab-server-proxy``. This provides the launcher icons in
   JupyterLab.

#. Various python packages in ``contrib/``. These are convenience packages that help set up
   a particular application for use - such as RStudio or Theia.

We try to keep the version numbers of all these packages in sync, even when there are no
changes. This keeps reasoning about versions simple.

Gaining Access Privileges
=========================

Before making a release, you need access privileges for the following.

#. Write access to the `GitHub repo <https://github.com/jupyterhub/jupyter-server-proxy>`_.

#. Publish access to the various python packages on PyPI.

#. Publish access to the JupyterLab plugin on `NPM <https://www.npmjs.com/>`_.

Release checklist
=================

#. Update the package version number in ``setup.py``.

#. Update the JupyterLab plugin's version to match, in ``jupyterlab-server-proxy/package.json``.
   We keep these two versions in sync to avoid figuring out a matrix of 'which version of
   the python package is compatible with which version of the JupyterLab plugin?'

#. Commit these changes and make a pull request with it. 

#. Once pull request is merged, make a tag of form ``v<version-number>``:

   .. code::

      git tag -a v<version-number>

   And push it to the official repository

   .. code::
     
      git push git@github.com:jupyterhub/jupyter-server-proxy --tags

#. Publish the package on PyPI

   .. code::

      pip install twine
      rm -rf dist/*
      python3 setup.py sdist bdist_wheel
      twine upload dist/*

#. Publish the JupyterLab plugin on npm

   .. code::

      cd jupyterlab-server-proxy
      npm install
      npm login
      npm publish

