# Contributing

Welcome! As a [Jupyter](https://jupyter.org) project, we follow the [Jupyter contributor guide](https://jupyter.readthedocs.io/en/latest/contributor/content-contributor.html).

To setup a local development environment and ru tests, see the small section in
the README.md file.

## Local development setup

### Python package

```bash
# Clone the repo to your local environment
git clone https://github.com/jupyterhub/jupyter-server-proxy.git
# Change directory to the jupyter-server-proxy directory
cd jupyter-server-proxy
# Install package in development mode
pip install -e ".[test]"
# Link your development version of the extension with JupyterLab
jupyter labextension develop --overwrite .
# Server extension must be manually installed in develop mode
jupyter server extension enable jupyter_server_proxy
```

Run the tests:

```bash
pytest
```

These generate test and coverage reports in `build/pytest` and `build/coverage`.

### Acceptance tests

If you have `robotframework-jupyterlibary` installed, the acceptance tests will run.

To install these in addition to the [Python package](#python-package) test
dependencies, run:

```bash
pip install -e ".[acceptance]"
```

In addition, compatible versions of:

- `geckodriver`
- `firefox`

Need to be on your `$PATH` and compatible with each other.

To run _only_ the acceptance tests, use the `-k` switch:

```bash
pytest -k acceptance
```

These are slower than the rest of the `pytest` tests, and generate screenshots,
browser logs, server logs, and report HTML in `build/robot`.

### JupyterLab extension

The `jlpm` command is JupyterLab's pinned version of `yarn` that is
installed with JupyterLab.

> You may use `yarn` or `npm run` instead of `jlpm` below.

```bash
cd labextension            # Change to the root of the labextension
jlpm                       # Install dependencies (or `npm i`)
jlpm build:prod            # Build:
                           # - `labextension/lib`
                           # - `jupyter_server_proxy/labextension`
jlpm install:extension     # Symlink into `{sys.prefix}/share/jupyter/labextensions`
```

You can watch the source directory and automatically rebuild the `labextension/lib`
and `jupyter_server_proxy/labextension` folders:

```bash
cd labextension
# Watch the source directory in one terminal, automatically rebuilding when needed
jlpm run watch
# Run JupyterLab in another terminal
jupyter lab
```

With the watch command running, every saved change will immediately be built locally
and available in your running JupyterLab. Refresh JupyterLab to load the change in
your browser (you may need to wait several seconds for the extension to be rebuilt).

By default, the `jlpm run build` command generates the source maps for this
extension to make it easier to debug using the browser dev tools. To also generate
source maps for the JupyterLab core extensions, you can run the following command:

```bash
jupyter lab build --minimize=False
```

### Documentation

The documentation uses a fairly standard [Sphinx](https://www.sphinx-doc.org)
build chain, and requires `make` on Linux/MacOS, which cannot be installed with
`pip`.

In addition to any system packages, building the documentation requires
additional packages. To install the needed packages:

```bash
pip install -r docs/requirements.txt
```

Once installed, enter the docs folder with:

```bash
cd docs
```

... then build the HTML site:

```bash
make
```

... or check that all hyperlinks can be resolved:

```bash
make linkcheck
```

... or start an auto-reloading server and open a web browser:

```bash
make devenv
```
