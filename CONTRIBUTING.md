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
jupyter server extension enable --sys-prefix jupyter_server_proxy
```

Before running tests, you need a server that we can test against.

```bash
JUPYTER_TOKEN=secret jupyter-lab --config=./tests/resources/jupyter_server_config.py --no-browser
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
pip install -e .[acceptance]
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
jlpm watch
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
