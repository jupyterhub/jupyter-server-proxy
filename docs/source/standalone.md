(standanlone)=

# Spawning and proxying a web service from JupyterHub

The `standalone` feature of Jupyter Server Proxy enables JupyterHub Admins to launch and proxy arbitrary web services
directly, in place of the JupyterLab or Notebook. You can use Jupyter Server Proxy to spawn a single proxy,
without it being attached to a Jupyter server. The proxy securely authenticates and restricts access to authorized
users through JupyterHub, giving a unified way to securely provide arbitrary applications.

This works similar to {ref}`proxying Server Processes <server-process>`, where a server process is started and proxied.
The Proxy is usually started from the command line, often by modifying the `Spawner.cmd` in your
[JupyterHub Configuration](https://jupyterhub.readthedocs.io/en/stable/tutorial/getting-started/spawners-basics.html).

This feature builds upon the work of [Dan Lester](https://github.com/danlester), who originally developed it in the
[jhsingle-native-proxy](https://github.com/ideonate/jhsingle-native-proxy) package.

## Installation

This feature has a dependency to JupyterHub and must be explicitly installed via an optional dependency:

```shell
pip install jupyter-server-proxy[standalone]
```

## Usage

The standalone proxy is controlled with the `jupyter standaloneproxy` command. You always need to specify the
{ref}`command <server-process:cmd>` of the web service that will be launched and proxied. Let's use
[voilà](https://github.com/voila-dashboards/voila) as an example here:

```shell
jupyter standaloneproxy -- voila --no-browser --port={port} /path/to/some/Notebook.ipynb
```

Executing this command will spawn a new HTTP Server, which will spawn the voilà dashboard and render the notebook.
Any template strings (like the `--port={port}`) inside the command will be automatically replaced when the command is
executed.

The CLI has multiple advanced options to customize the behavior of the proxy. Execute `jupyter standaloneproxy --help`
to get a complete list of all arguments.

### Specify address and port

The proxy will try to extract the address and port from the `JUPYTERHUB_SERVICE_URL` environment variable, which is
set if an application is launched by JupyterHub. Otherwise, it will be launched on `127.0.0.1:8888`.
You can also explicitly overwrite these values:

```shell
jupyter standaloneproxy --address=localhost --port=8000 ...
```

### Disable Authentication

For testing, it can be useful to disable the authentication with JupyterHub. Passing `--skip-authentication` will
not triggering the login process when accessing the application.

```{warning} Disabling authentication will leave the application open to anyone! Be careful with it,
especially on multi-user systems.
```

## Usage with JupyterHub

To launch a standalone proxy with JupyterHub, you need to customize the `Spawner` inside the configuration
using traitlets:

```python
c.Spawner.cmd = "jupyter-standaloneproxy"
c.Spawner.args = ["--", "voila", "--no-browser", "--port={port}", "/path/to/some/Notebook.ipynb"]
```

This will hard-code JupyterHub to launch voilà instead of `jupyterhub-singleuser`. In case you want to give the users
of the JupyterHub the ability to select which application to launch (like selecting either JupyterLab or voilà),
you will want to make this configuration optional:

```python
# Let users select which application start
c.Spawner.options_form = """
        <label for="select-application">Choose Application: </label>
        <select name="application" required>
            <option value="lab">JupyterLab</option>
            <option value="voila">voila</option>
        </select>
    """

def select_application(spawner):
    application = spawner.user_options.get("application", ["lab"])[0]
    if application == "voila":
        spawner.cmd = "jupyter-standaloneproxy"
        spawner.args = ["--", "voila", "--no-browser", "--port={port}", "/path/to/some/Notebook.ipynb"]

c.Spawner.pre_spawn_hook = select_application
```

```{note} This is only a very basic implementation to show a possible approach. For a production setup, you can create
a more rigorous implementation by creating a custom `Spawner` and overwriting the appropriate functions and/or
creating a custom `spawner.html` page.
```

## Technical Overview

The following section should serve as an explanation to developers of the standalone feature of jupyter-server-proxy.
It outlines the basic functionality and will explain the different components of the code in more depth.

### JupyterHub and jupyterhub-singleuser

By default, JupyterHub will use the `jupyterhub-singleuser` executable when launching a new instance for a user.
This executable is usually a wrapper around the `JupyterLab` or `Notebook` application, with some
additions regarding authentication and multi-user systems.
In the standalone feature, we try to mimic these additions, but instead of using `JupyterLab` or `Notebook`, we
will wrap them around an arbitrary web application.
This will ensure only authenticated access to the application, while providing direct access to the application
without needing a Jupyter server to be running in the background.
The different additions will be discussed in more detail below.

### Structure

The standalone feature is built on top of the `SuperviseAndProxyhandler`, which will spawn a process and proxy
requests to this server. While this process is called _Server_ in the documentation, I will call it _Application_
here, to avoid confusion with the other server where the `SuperviseAndProxyhandler` is attached to.
When using jupyter-server-proxy, the proxies are attached to the Jupyter server and will proxy requests
to the application.
Since we do not want to use the Jupyter server here, we instead require an alternative server, which will be used
to attach the `SuperviseAndProxyhandler` and all the required additions from `jupyterhub-singleuser`.
For that, we use tornado `HTTPServer`.

### Login and Authentication

One central component is the authentication with the JupyterHub Server.
Any client accessing the application will need to authenticate with the JupyterHub API, which will ensure only
the user themselves (or otherwise allowed users, e.g., admins) can access the application.
The Login process is started by deriving our `StandaloneProxyHandler` from
[jupyterub.services.auth.HubOAuthenticated](https://github.com/jupyterhub/jupyterhub/blob/5.0.0/jupyterhub/services/auth.py#L1541)
and decorating any methods we want to authenticate with `tornado.web.authenticated`.
For the proxy, we just decorate the `proxy` method with `web.authenticated`, which will authenticate all routes on all HTTP Methods.
`HubOAuthenticated` will automatically provide the login URL for the authentication process and any
client accessing any path of our server will be redirected to the JupyterHub API.

After a client has been authenticated with the JupyterHub API, they will be redirected back to our server.
This redirect will be received on the `/oauth_callback` path, from where we need to redirect the client back to the
root of the application.
We use the [HubOAuthCallbackHander](https://github.com/jupyterhub/jupyterhub/blob/5.0.0/jupyterhub/services/auth.py#L1547),
another handler from the JupyterHub package, for this.
It will also cache the received OAuth state from the login, so that we can skip authentication for the next requests
and do not need to go through the whole login process for each request.

### SSL certificates

In some JupyterHub configurations, the launched application will be configured to use an SSL certificate for request
between the JupyterLab / Notebook and the JupyterHub API. The path of the certificate is given in the
`JUPYTERHUB_SSL_*` environment variables. We use these variables to create a new SSL Context for both
the `AsyncHTTPClient` (used for Activity Notification, see below) and the `HTTPServer`.

### Activity Notifications

The `jupyterhub-singleuser` will periodically send an activity notification to the JupyterHub API and inform it that
the currently running application is still active. Whether this information is actually used or not depends on the
specific configuration of this JupyterHub.

### Environment Variables

JupyterHub uses a lot of environment variables to specify how the launched app should be run.
This list is a small overview of all used variables and what they contain and are used for.

| Variable                                                                        | Explanation                                                                                                                                                                           | Typical Value                              |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| `JUPYTERHUB_SERVICE_URL`                                                        | URL where the server should be listening. Used to find the Address and Port to start the server on.                                                                                   | `http://127.0.0.1:5555`                    |
| `JUPYTERHUB_SERVICE_PREFIX`                                                     | An URL Prefix where the root of the launched application should be hosted. E.g., when set to `/user/name/`, then the root of the proxied aplication should be `/user/name/index.html` | `/services/service-name/` or `/user/name/` |
| `JUPYTERHUB_ACTIVITY_URL`                                                       | URL where to send activity notifications to.                                                                                                                                          | `$JUPYTERHUB_API_URL/user/name/activity`   |
| `JUPYTERHUB_API_TOKEN`                                                          | Authorization Token for requests to the JupyterHub API.                                                                                                                               |                                            |
| `JUPYTERHUB_SERVER_NAME`                                                        | A name given to all apps launched by the JupyterHub.                                                                                                                                  |                                            |
| `JUPYTERHUB_SSL_KEYFILE`, `JUPYTERHUB_SSL_CERTFILE`, `JUPYTERHUB_SSL_CLIENT_CA` | Paths to keyfile, certfile and client CA for the SSL configuration                                                                                                                    |                                            |
| `JUPYTERHUB_USER`, `JUPYTERHUB_GROUP`                                           | Name and Group of the user for this application. Required for Authentication                                                                                                          |
