# Contributing

Welcome! As a [Jupyter](https://jupyter.org) project, we follow the [Jupyter contributor guide](https://jupyter.readthedocs.io/en/latest/contributor/content-contributor.html).

To setup a local development environment and ru tests, see the small section in
the README.md file.

## Local development setup

### Python package

```bash
pip install -e .[test]

# explicit install needed with editable mode (-e) jupyter
jupyter serverextension enable --sys-prefix jupyter_server_proxy
```

Before running tests, you need a [notebook
server](https://github.com/jupyter/notebook) that we can test against.

```
JUPYTER_TOKEN=secret jupyter-notebook --config=./tests/resources/jupyter_server_config.py
```

Run the tests:

```bash
pytest --verbose
```

These generate test and coverage reports in `build/pytest` and `build/coverage`.

### Acceptance tests

If you have `robotframework-jupyterlibary` installed, the acceptance tests will run.

To install these in addition to the [Python package](#python-package) test
dependencies, run:

```bash
pip install -e .[test,acceptance]
```

In addition, compatible versions of:
- `geckodriver`
- `firefox`

Needs to be on your `$PATH` and compatible with each other.

To run _only_ the acceptance tests, use the `-k` switch:

```bash
pytest -k acceptance
```

These are slower than the rest of the `pytest` tests, and generate screenshots,
browser logs, server logs, and report HTML in `build/robot`.

### JupyterLab extension

The `jlpm` command is JupyterLab's pinned version of `yarn` that is
installed with JupyterLab. You may use `yarn` or `npm` instead of `jlpm`
below.

```bash
cd jupyterlab-server-proxy

# Install dependencies
jlpm

# Build Typescript source
jlpm build

# Link your development version of the extension with JupyterLab
jupyter labextension link .

# Rebuild Typescript source after making changes
jlpm build

# Rebuild JupyterLab after making any changes
jupyter lab build
```

You can watch the source directory and run JupyterLab in watch mode to
watch for changes in the extension's source and automatically rebuild
the extension and application.

```bash
# Watch the source directory in another terminal tab
jlpm watch

# Run jupyterlab in watch mode in one terminal tab
jupyter lab --watch
```
