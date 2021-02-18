"""
jupyter-server-proxy setup
"""
import json
from glob import glob
from pathlib import Path

import setuptools
from jupyter_packaging import (
    combine_commands,
    create_cmdclass,
    ensure_targets,
    install_npm,
    skip_if_exists,
)

HERE = Path(__file__).parent.resolve()

# The name of the project
name = "jupyter_server_proxy"

lab_path = HERE / name / "labextension"

# Representative files that should exist after a successful build
jstargets = [
    str(lab_path / "package.json"),
]

package_data_spec = {
    name: ["*"],
}

labext_name = "@jupyterlab/server-proxy"

data_files_spec = [
    ("share/jupyter/labextensions/%s" % labext_name, str(lab_path), "**"),
    ("share/jupyter/labextensions/%s" % labext_name, str(HERE), "install.json"),
    (
        "etc/jupyter/jupyter_server_config.d",
        "jupyter_server_proxy/etc",
        "jupyter-server-proxy-jupyterserverextension.json",
    ),
    (
        "etc/jupyter/jupyter_notebook_config.d",
        "jupyter_server_proxy/etc",
        "jupyter-server-proxy-notebookserverextension.json",
    ),
    (
        "etc/jupyter/nbconfig/tree.d",
        "jupyter_server_proxy/etc",
        "jupyter-server-proxy-nbextension.json",
    ),
]

cmdclass = create_cmdclass(
    "jsdeps", package_data_spec=package_data_spec, data_files_spec=data_files_spec
)

js_command = combine_commands(
    install_npm(HERE / "jupyterlab-server-proxy", build_cmd="build:prod", npm=["jlpm"]),
    ensure_targets(jstargets),
)

is_repo = (HERE / ".git").exists()
if is_repo:
    cmdclass["jsdeps"] = js_command
else:
    cmdclass["jsdeps"] = skip_if_exists(jstargets, js_command)

long_description = (HERE / "README.md").read_text()

# Get the package info from package.json
pkg_json = json.loads((HERE / "jupyterlab-server-proxy" / "package.json").read_bytes())

setup_args = dict(
    name=name,
    version=pkg_json["version"],
    url=pkg_json["homepage"],
    author=pkg_json["author"]["name"],
    author_email=pkg_json["author"]["email"],
    description=pkg_json["description"],
    license=pkg_json["license"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    cmdclass=cmdclass,
    packages=setuptools.find_packages(),
    install_requires=["simpervisor>=0.4", "aiohttp"],
    zip_safe=False,
    include_package_data=True,
    python_requires=">=3.6",
    keywords=["Jupyter", "JupyterLab", "JupyterLab3"],
    classifiers=[
        "Framework :: Jupyter",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: Jupyter",
    ],
    data_files=[
        ("share/jupyter/nbextensions/jupyter_server_proxy", glob("jupyter_server_proxy/static/*")),
        (
            "etc/jupyter/jupyter_notebook_config.d",
            ["jupyter_server_proxy/etc/jupyter-server-proxy-notebookserverextension.json"],
        ),
        (
            "etc/jupyter/jupyter_server_config.d",
            ["jupyter_server_proxy/etc/jupyter-server-proxy-jupyterserverextension.json"],
        ),
        (
            "etc/jupyter/nbconfig/tree.d",
            ["jupyter_server_proxy/etc/jupyter-server-proxy-nbextension.json"],
        ),
    ],
)


if __name__ == "__main__":
    setuptools.setup(**setup_args)
