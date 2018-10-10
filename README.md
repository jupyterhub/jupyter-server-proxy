# nbserverproxy
Jupyter notebook server extension to proxy web services. This enables users to reach arbitrary web services running within their spawned Jupyter server and is probably most appropriate for services which can't readily be converted into extensions.

## Example
A user starts a web service via `New > Terminal`:
```
echo "hello world" > index.html
python -m http.server 8001
```
The service is proxied off to `/proxy/` and can be reached at
* https://address.of.notebook.server/user/theuser/proxy/8001 when running inside a JupyterHub
* http://localhost:8888/proxy/8001 when running locally

## Installation
nbserverproxy requires python3.

Install via pip:
```
pip install nbserverproxy
```

Or via conda:
```
conda install -c conda-forge nbserverproxy
```

Then enable:
```
jupyter serverextension enable --py nbserverproxy
```

Based on https://github.com/senko/tornado-proxy.
