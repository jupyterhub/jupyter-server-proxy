(launchers)=

# GUI Launchers

Jupyter Server Proxy automatically adds entries for {ref}`registered
Server Processes <server-process>` in both the classic Jupyter Notebook
interface and the JupyterLab Launcher.

## Classic Notebook Extension

By default, an entry is made for each server process under the 'New'
menu in the notebook's default tree view. Note that a new instance
is **not** launched every time you click an item - if the process
is already running, it is reused.

```{image} _static/images/nbextension-tree.png

```

## JupyterLab Extension

A JupyterLab extension is bundled with the Python package to provide launch
buttons in JupyterLab's Launcher panel for registered server processes.

```{image} _static/images/labextension-launcher.png

```

Clicking on them opens the proxied application in a new browser window.

Currently running proxy applications are shown in the running sessions tab
under "Server Proxy Apps" section.

```{image} _static/images/labextension-manager.gif

```

As shown in the GIF, users can consult the metadata of each running proxy
application by hovering over the name of the proxy. It is also possible to
terminate the proxy application using Shut Down button.

```{note}
When the user clicks Shut Down button to terminate a proxy application,
a `SIGTERM` signal is sent to the application. It is the user's responsibility
to ensure that the application exits cleanly with a `SIGTERM` signal. There
are certain applications (like MLflow) that cannot be terminted with `SIGTERM`
signal and in those cases, the users can setup wrapper scripts to trap the
signal and ensure clean teardown of the application.
```

The lab extension manager will poll for running proxy applications at a
given interval which can be configured using Jupyter Server Proxy settings.
By default this is set to 10 seconds. Users can change
this interval by changing `Auto-refresh rate` in `Jupyter Server Proxy`
section in `Advanced Settings Editor` in JupyterLab UI.

```{image} _static/images/labextension-settings.png

```

Only proxy applications that are started by `jupyter-server-proxy` are shown
in the running Server Proxy Apps section.
