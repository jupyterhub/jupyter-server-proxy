import setuptools

setuptools.setup(
    name="jupyter-theia-proxy",
    version='1.0dev',
    url="https://github.com/jupyterhub/jupyter-server-proxy/tree/master/contrib/theia",
    author="Project Jupyter Contributors",
    description="projectjupyter@gmail.com",
    packages=setuptools.find_packages(),
	keywords=['Jupyter'],
	classifiers=['Framework :: Jupyter'],
    install_requires=[
        'jupyter-server-proxy'
    ],
    entry_points={
        'jupyter_serverproxy_servers': [
            'theia = jupyter_theia_proxy:setup_theia',
        ]
    },
    package_data={
        'jupyter_theia_proxy': ['icons/*'],
    },
)
