# nbrsessionproxy
![Screenshot](screenshot.png)

Jupyter extensions to proxy RStudio's rsession. Requires [nbserverproxy](https://github.com/ryanlovett/nbrsessionproxy) and currently assumes an Ubuntu environment.

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
