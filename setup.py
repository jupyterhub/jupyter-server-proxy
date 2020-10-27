import setuptools
from glob import glob

setuptools.setup(
    name="jupyter-server-proxy",
    version='1.5.2',
    url="https://github.com/jupyterhub/jupyter-server-proxy",
    author="Ryan Lovett & Yuvi Panda",
    author_email="rylo@berkeley.edu",
    license="BSD 3-Clause",
    description="Jupyter server extension to supervise and proxy web services",
    packages=setuptools.find_packages(),
    install_requires=['notebook', 'simpervisor>=0.2', 'aiohttp'],
    python_requires='>=3.5',
    classifiers=[
        'Framework :: Jupyter',
    ],
    data_files=[
        ('share/jupyter/nbextensions/jupyter_server_proxy', glob('jupyter_server_proxy/static/*')),
        ('etc/jupyter/jupyter_notebook_config.d', ['jupyter_server_proxy/etc/jupyter-server-proxy-serverextension.json']),
        ('etc/jupyter/nbconfig/tree.d', ['jupyter_server_proxy/etc/jupyter-server-proxy-nbextension.json'])
    ],
    include_package_data=True,
    zip_safe=False
)
