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

#. **icon**

   Full path to an icon in SVG format that may be optionally used to
   represent this server in UI.


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
   in your notebook url.
   
