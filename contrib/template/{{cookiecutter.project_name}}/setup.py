import setuptools

setuptools.setup(
    name="jupyter-{{cookiecutter.project_name}}-proxy",
    version='1.0dev',
    url="https://github.com/jupyterhub/jupyter-server-proxy/tree/master/contrib/{{cookiecutter.project_name}}",
    author="{{cookiecutter.author_name}}",
    description="{{cookiecutter.author_email}}",
    packages=setuptools.find_packages(),
	keywords=['Jupyter'],
	classifiers=['Framework :: Jupyter'],
    install_requires=[
        'jupyter-server-proxy'
    ],
    entry_points={
        'jupyter_serverproxy_servers': [
            '{{cookiecutter.project_name}} = jupyter_{{cookiecutter.project_name}}_proxy:setup_{{cookiecutter.project_name}}',
        ]
    },
    package_data={
        'jupyter_{{cookiecutter.project_name}}_proxy': ['icons/*'],
    },
)
