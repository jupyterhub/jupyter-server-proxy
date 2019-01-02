import setuptools
from glob import glob

setuptools.setup(
    name="nbserverproxy",
    version='0.8.8',
    url="https://github.com/jupyterhub/nbserverproxy",
    author="Ryan Lovett & Yuvi Panda",
    author_email="rylo@berkeley.edu",
    license="BSD 3-Clause",
    description="Jupyter server extension to proxy web services",
    packages=setuptools.find_packages(),
    install_requires=['notebook', 'simpervisor', 'aiohttp'],
    python_requires='>=3.5',
    classifiers=[
        'Framework :: Jupyter',
    ],
    data_files=[
        ('share/jupyter/nbextensions/nbserverproxy', glob('nbserverproxy/static/*')),
        ('etc/jupyter/jupyter_notebook_config.d', ['nbserverproxy/etc/serverextension.json']),
        ('etc/jupyter/nbconfig/notebook.d', ['nbserverproxy/etc/nbextension.json'])
    ],
    include_package_data=True,
    zip_safe=False
)
