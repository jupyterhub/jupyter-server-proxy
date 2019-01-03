.. _server-process:

=============================
Starting & Proxying processes
=============================

Jupyter Server Proxy can start & supervise the process providing
the web service it is proxying. The process is started the first
time an appropriate URL is requested, and restarted if it fails.

Processes that are supervised and proxied are called **servers**.
They can be configured either in the notebook configuration, or
as separate packages.

Server Process options
======================

Server Processes are configured with a dictionary of key value
pairs.

#. **command**

   One of:

   * A list of strings that is the command used to start the
     process. If the string ``{port}`` is present anywhere, it'll
     be replaced with the port the process should listen on.
    
   * A callable that takes one parameter - ``port``, and returns a
     list of strings that are used & treated same as above.
  
   This key is required.

#. **environment**

   One of:

   * A dictionary of strings that are passed in as the environment to
     the started process, in addition to the environment of the notebook
     process itself. If the string ``{port}}`` is present anywhere,
     it'll be replaced with the port the process should listen on.

   * A callable that takes on parameter - ``port``, and returns a dictionary
     of strings that are used & treated same as above.

#. **launcher_entry**

   A dictionary with options on if / how an entry in the classic Jupyter Notebook
   'New' dropdown or the JupyterLab launcher should be added. It can contain
   the following keys:

   #. **enabled**
      Set to True (default) to make an entry in the launchers. Set to False to have no
      explicit entry.

   #. **icon_path**
      Full path to an svg icon that could be used with a launcher. Currently only used by the
      JupyterLab launcher

   #. **title**
      Title to be used for the launcher entry. Defaults to the name of the server if missing.

Specifying config via traitlets
===============================

[Traitlets](https://traitlets.readthedocs.io/) are the configuration
mechanism used by Jupyter Notebook. It can take config in Python
and we can use that to specify Server Processes - including functions
if we want tighter control over what process is spawned.

#. Create a file called ``jupyter_notebook_config.py`` in one of the
   Jupyter config directories. You can get a list of these directories
   by running ``jupyter --paths`` and looking under the 'config'
   section

#. Add your Server Process configuration there by setting
   ``c.ServerProxy.servers`` traitlet.

   For example,

   .. code:: python

      c.ServerProxy.servers = {
        'openrefine': {
          'command': ['refine', '-p', '{port}']
        }
      }

   This will start `OpenRefine <http://openrefine.org/>`_ with the
   ``refine`` command (which must be in $PATH) on a randomly
   generated port, and make it available under ``/openrefine``
   in your notebook url. The URL path is specified by the key,
   but this should be made more configurable in the future.

Specifying config from python packages
======================================

It is often convenient to provide the Server Process configuration
as a python package, so users can simply ``pip install`` it.
This is possible, thanks to `the magic of entrypoints
<https://amir.rachum.com/blog/2017/07/28/python-entry-points/>`_.

We'll work through it by repeating the OpenRefine example from
above.

#. Create a python file named ``openrefine.py``

   .. code:: python

    def setup_openrefine():
      return {
        'command': ['refine', '-p', '{port}']
      }

   A simple function that returns a Server Process configuration
   dictionary when called. This can return any kind of Server
   Process configuration dictionary, and include functions easily.

#. Make an appropriate ``setup.py``

   .. code:: python

      import setuptools

      setuptools.setup(
        name="jupyter-openrefine-server",
        # py_modules rather than packages, since we only have 1 file
        py_modules=['openrefine'],
        entry_points={
            'jupyter_serverproxy_servers': [
                # name = packagename:function_name
                'openrefine = openrefine:setup_openrefine',
            ]
        },
      )

   We make an entry for the ``jupyter_serverproxy_servers`` entrypoint.
   When jupyter-server-proxy starts up, it goes through the list of
   entrypoint entries from all installed packages & sets itself up
   with all the Server Process configurations.

#. You can now test this out with ``pip install .``, making sure you
   are in the same environment as the jupyter notebook process. If you
   go to ``<notebook-url>/openrefine`` (and have OpenRefine installed
   and in ``$PATH``!), you should see an instance of OpenRefine!
