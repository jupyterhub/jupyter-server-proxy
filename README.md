# nbrsessionproxy
![Screenshot](screenshot.png)

Jupyter server and notebook extensions to proxy RStudio's rsession. This is useful if you have deployed JupyterHub and would like to take advantage of its existing authenticator and spawner to launch RStudio in users' Jupyter environments. You can also run this from within Jupyter. Requires [nbserverproxy](https://github.com/jupyterhub/nbserverproxy).

Note that [RStudio Server Pro](https://www.rstudio.com/products/rstudio-server-pro/architecture) has more featureful authentication and spawning than the standard version, in the event that you do not want to use Jupyter.

## Installation
Install the library:
```
pip install git+https://github.com/ryanlovett/nbrsessionproxy
```

Install the extensions for the user:
```
jupyter serverextension enable  --py nbrsessionproxy
jupyter nbextension     install --py nbrsessionproxy
jupyter nbextension     enable  --py nbrsessionproxy
```

Install the extensions for all users on the system:
```
pip install git+https://github.com/ryanlovett/nbrsessionproxy
jupyter serverextension enable  --py --sys-prefix nbrsessionproxy
jupyter nbextension     install --py --sys-prefix nbrsessionproxy
jupyter nbextension     enable  --py --sys-prefix nbrsessionproxy
```
