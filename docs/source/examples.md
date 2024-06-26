(examples)=

# Examples

If you are looking for examples on how to configure `jupyter-server-proxy`, you might want to check existing
projects on GitHub, such as:

- [jupyter-pgweb-proxy](https://github.com/illumidesk/jupyter-pgweb-proxy): Run [pgweb](https://github.com/sosedoff/pgweb) (cross-platform PostgreSQL client)
- [jupyter-pluto-proxy](https://github.com/illumidesk/jupyter-pluto-proxy): Run [Pluto.jl](https://github.com/fonsp/Pluto.jl) (notebooks for Julia)
- [jupyterserverproxy-openrefine](https://github.com/psychemedia/jupyterserverproxy-openrefine): Run [OpenRefine](https://openrefine.org/) (tool for working with messy data)
- [gator](https://github.com/mamba-org/gator): Run the Mamba Navigator (JupyterLab-based standalone application)

Projects can also add the `jupyter-server-proxy` topic to the GitHub repository to make it more discoverable:
[https://github.com/topics/jupyter-server-proxy](https://github.com/topics/jupyter-server-proxy)

# Test the proxy setup

If you just want to test if the proxy config is correct you can put the following into `$HOME/.jupyter/jupyter_server_config.py`:
```python
c.ServerProxy.servers.update({
    "pythonweb": {
    "command": ["/usr/local/anaconda/bin/python", "-m", "http.server", "{port}"],
    "port": 9081,
    "absolute_url": False
    }
})
```
You should then get a new button in the launcher. Putting it into `/etc/jupyter` will make it available to all users.
