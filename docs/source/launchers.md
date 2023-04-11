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
