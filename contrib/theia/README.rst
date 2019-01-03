=========
Theia IDE
=========

`Theia <https://www.theia-ide.org/>`_ is a configurable web based IDE
built with components from `Visual Studio Code <https://code.visualstudio.com/>`_.

This package is a plugin for `jupyter-server-proxy <https://jupyter-server-proxy.readthedocs.io/>`_
that lets you run an instance of theia alongside your notebook, primarily
in a JupyterHub / Binder environment.

Installing Theia
================

#. `Install the ``yarn`` package manager <https://yarnpkg.com/lang/en/docs/install/#alternatives-stable>`_
    with one of the available methods.

#. Theia is highly configurable, so you need to decide which features you want
   in your theia install. Make a ``package.json`` with the list of extensions you want,
   following `the instructions here <https://www.theia-ide.org/doc/Composing_Applications.html>`_.

   Here is an example:


   .. code:: js

      {
        "private": true,
        "dependencies": {
            "@theia/callhierarchy": "latest",
            "@theia/editor-preview": "latest",
            "@theia/file-search": "latest",
            "@theia/git": "latest",
            "@theia/json": "latest",
            "@theia/languages": "latest",
            "@theia/markers": "latest",
            "@theia/merge-conflicts": "latest",
            "@theia/messages": "latest",
            "@theia/mini-browser": "latest",
            "@theia/monaco": "latest",
            "@theia/navigator": "latest",
            "@theia/outline-view": "latest",
            "@theia/preferences": "latest",
            "@theia/preview": "latest",
            "@theia/python": "latest",
            "@theia/search-in-workspace": "latest",
            "@theia/terminal": "latest",
            "@theia/textmate-grammars": "latest",
            "@theia/typescript": "latest",
            "typescript": "latest",
            "yarn": "^1.12.3"
        },
        "devDependencies": {
            "@theia/cli": "latest"
        }
      }

#. Run the following commands in the same location as your package.json file
   to install all packages & build theia.

   .. code:: bash
      
      yarn
      yarn theia build

   This should set up theia to run and be built.

#. Add the ``node_modules/.bin`` directory to your ``$PATH``, so ``jupyter-theia-proxy`` can
   find the ``theia`` command.

   .. code:: bash

      export PATH="$(pwd)/node_modules/.bin:${PATH}"