(server-process)=

# Starting & Proxying processes

Jupyter Server Proxy can start & supervise the process providing
the web service it is proxying. The process is started the first
time an appropriate URL is requested, and restarted if it fails.

Processes that are supervised and proxied are called **servers**.
They can be configured either in the notebook configuration, or
as separate packages.

## Server Process options

Server Processes are configured with a dictionary of key value
pairs.

(server-process:cmd)=

### `command`

One of:

- A list of strings that is the command used to start the
  process. The following template strings will be replaced:

  - `{port}` the port that the process should listen on. This will be 0 if it
    should use a Unix socket instead.
  - `{unix_socket}` the path at which the process should listen on a Unix
    socket. This will be an empty string if it should use a TCP port.
  - `{base_url}` the base URL of the notebook. For example, if the application
    needs to know its full path it can be constructed from
    `{base_url}/proxy/{port}`

- A callable that takes any {ref}`callable arguments <server-process:callable-arguments>`,
  and returns a list of strings that are used & treated same as above.

If the command is not specified or is an empty list, the server process is
assumed to be started ahead of time and already available to be proxied to.

### `timeout`

Timeout in seconds for the process to become ready, default `5`.

A process is considered 'ready' when it can return a valid HTTP response on the
port it is supposed to start at.

### `environment`

One of:

- A dictionary of strings that are passed in as the environment to
  the started process, in addition to the environment of the notebook
  process itself. The strings `{port}`, `{unix_socket}` and
  `{base_url}` will be replaced as for **command**.
- A callable that takes any {ref}`callable arguments <server-process:callable-arguments>`,
  and returns a dictionary of strings that are used & treated same as above.

### `absolute_url`

_True_ if the URL as seen by the proxied application should be the full URL
sent by the user. _False_ if the URL as seen by the proxied application should
see the URL after the parts specific to jupyter-server-proxy have been stripped.

For example, with the following config:

```python
c.ServerProxy.servers = {
    "test-server": {
        "command": ["python3", "-m", "http.server", "{port}"],
        "absolute_url": False
    }
}
```

When a user requests `/test-server/some-url`, the proxied server will see it
as a request for `/some-url` - the `/test-server` part is stripped out.

If `absolute_url` is set to `True` instead, the proxied server will see it
as a request for `/test-server/some-url` instead - without any stripping.

This is very useful with applications that require a `base_url` to be set.

Defaults to _False_.

### `port`

Set the port that the service will listen on. The default is to
automatically select an unused port.

(server-process:unix-socket)=

### `unix_socket`

This option uses a Unix socket on a filesystem path, instead of a TCP
port. It can be passed as a string specifying the socket path, or _True_ for
Jupyter Server Proxy to create a temporary directory to hold the socket,
ensuring that only the user running Jupyter can connect to it.

If this is used, the `{unix_socket}` argument in the command template
(see {ref}`server-process:cmd`) will be a filesystem path. The server should
create a Unix socket bound to this path and listen for HTTP requests on it.
The `port` configuration key will be ignored.

```{note}
Proxying websockets over a Unix socket requires Tornado >= 6.3.
```

### `mappath`

Map request paths to proxied paths.
Either a dictionary of request paths to proxied paths,
or a callable that takes parameter `path` and returns the proxied path.

### `launcher_entry`

A dictionary with options on if / how an entry in the classic Jupyter Notebook
'New' dropdown or the JupyterLab launcher should be added. It can contain
the following keys:

1. **enabled**
   Set to True (default) to make an entry in the launchers. Set to False to have no
   explicit entry.
2. **icon_path**
   Full path to an svg icon that could be used with a launcher. Currently only used by the
   JupyterLab launcher, when category is "Notebook" (default) or "Console".
3. **title**
   Title to be used for the launcher entry. Defaults to the name of the server if missing.
4. **path_info**
   The trailing path that is appended to the user's server URL to access the proxied server.
   By default it is the name of the server followed by a trailing slash.
5. **category**
   The category for the launcher item. Currently only used by the JupyterLab launcher.
   By default it is "Notebook".

### `new_browser_tab`

_JupyterLab only_ - _True_ (default) if the proxied server URL should be opened in a new browser tab.
_False_ if the proxied server URL should be opened in a new JupyterLab tab.

If _False_, the proxied server needs to allow its pages to be rendered in an iframe. This
is generally done by configuring the web server `X-Frame-Options` to `SAMEORIGIN`.
For more information, refer to
[MDN Web docs on X-Frame-Options](https://developer.mozilla.org/docs/Web/HTTP/Headers/X-Frame-Options).

Note that applications might use a different terminology to refer to frame options.
For example, RStudio uses the term _frame origin_ and require the flag
`--www-frame-origin=same` to allow rendering of its pages in an iframe.

### `request_headers_override`

One of:

- A dictionary of strings that are passed in as HTTP headers to the proxy
  request. The strings `{port}` and `{base_url}` will be replaced as
  for **command**.
- A callable that takes any {ref}`callable arguments <server-process:callable-arguments>`,
  and returns a dictionary of strings that are used & treated same as above.

### `update_last_activity`

Whether to report activity from the proxy to Jupyter Server. If _True_, Jupyter Server
will be notified of new activity. This is primarily used by JupyterHub for idle detection and culling.

Useful if you want to have a seperate way of determining activity through a
proxied application.

Defaults to _True_.

(server-process:callable-arguments)=

### `raw_socket_proxy`

_True_ to proxy only websocket connections into raw stream connections.
_False_ (default) if the proxied server speaks full HTTP.

If _True_, the proxied server is treated a raw TCP (or unix socket) server that
does not use HTTP.
In this mode, only websockets are handled, and messages are sent to the backend
server as raw stream data. This is similar to running a
[websockify](https://github.com/novnc/websockify) wrapper.
All other HTTP requests return 405.

#### Callable arguments

Any time you specify a callable in the config, it can ask for any arguments it needs
by simply declaring it - only arguments the callable asks for will be passed to it.

For example, with the following config:

```python
def _cmd_callback():
    return ["some-command"]

server_config = {
    "command": _cmd_callback
}
```

No arguments will be passed to `_cmd_callback`, since it doesn't ask for any. However,
with:

```python
def _cmd_callback(port):
    return ["some-command", "--port=" + str(port)]

server_config = {
    "command": _cmd_callback
}
```

The `port` argument will be passed to the callable. This is a simple form of dependency
injection that helps us add more parameters in the future without breaking backwards
compatibility.

##### Available arguments

Currently, the following arguments are available:

1. **port**
   The port the command should listen on
2. **base_url**
   The base URL of the notebook

If any of the returned strings, lists or dictionaries contain strings
of form `{<argument-name>}`, they will be replaced with the value
of the argument. For example, if your function is:

```python
def _openrefine_cmd():
    return ["openrefine", "-p", "{port}"]
```

The `{port}` will be replaced with the appropriate port before
the command is started

## Specifying config via traitlets

[Traitlets](https://traitlets.readthedocs.io/) are the configuration
mechanism used by Jupyter Notebook. It can take config in Python
and we can use that to specify Server Processes - including functions
if we want tighter control over what process is spawned.

1. Create a file called `jupyter_server_config.py` in one of the
   Jupyter config directories. You can get a list of these directories
   by running `jupyter --paths` and looking under the 'config'
   section

2. Add your Server Process configuration there by setting
   `c.ServerProxy.servers` traitlet.

   For example,

   ```python
   c.ServerProxy.servers = {
      "openrefine": {
          "command": ["refine", "-p", "{port}"]
      }
   }
   ```

   This will start [OpenRefine](https://openrefine.org/) with the
   `refine` command (which must be in \$PATH) on a randomly
   generated port, and make it available under `/openrefine`
   in your notebook url. The URL path is specified by the key,
   but this should be made more configurable in the future.

(server-process:package)=

## Specifying config from python packages

It is often convenient to provide the Server Process configuration
as a python package, so users can simply `pip install` it.
This is possible, thanks to [the magic of entrypoints](https://amir.rachum.com/blog/2017/07/28/python-entry-points/).

We'll work through it by repeating the OpenRefine example from
above.

1. Create a python file named `openrefine.py`

   ```python
   def setup_openrefine():
      return {
          "command": ["refine", "-p", "{port}"]
      }
   ```

   A simple function that returns a Server Process configuration
   dictionary when called. This can return any kind of Server
   Process configuration dictionary, and include functions easily.

2. Make an appropriate `setup.py`

   ```python
   import setuptools

   setuptools.setup(
      name="jupyter-openrefine-server",
      # py_modules rather than packages, since we only have 1 file
      py_modules=["openrefine"],
      entry_points={
          "jupyter_serverproxy_servers": [
              # name = packagename:function_name
              "openrefine = openrefine:setup_openrefine",
          ]
      },
      install_requires=["jupyter-server-proxy"],
   )
   ```

   We make an entry for the `jupyter_serverproxy_servers` entrypoint.
   When jupyter-server-proxy starts up, it goes through the list of
   entrypoint entries from all installed packages & sets itself up
   with all the Server Process configurations.

3. You can now test this out with `pip install .`, making sure you
   are in the same environment as the jupyter notebook process. If you
   go to `<notebook-url>/openrefine` (and have OpenRefine installed
   and in `$PATH`!), you should see an instance of OpenRefine!
