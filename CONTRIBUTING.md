# Contributing

Welcome! As a [Jupyter](https://jupyter.org) project, we follow the [Jupyter contributor guide](https://jupyter.readthedocs.io/en/latest/contributor/content-contributor.html).

To setup a local development environment and run tests, see the small section in
the README.md file.

## Local development setup

### `conda`

<details>

<summary>
<i>
Optional, but especially recommended on non-Linux platforms...
</i>
</summary>

Using the `conda` (or `mamba` or `micromamba`) package manager with packages from
[`conda-forge`](https://conda-forge.org/feedstock-outputs) can help isolate development
environments on nearly any operating system and architecture.

For example, after installing [`mambaforge`](https://conda-forge.org/miniforge),
create a new environment with all heavy development and test dependencies:

```yaml
mamba create --name=jupyter-server-proxy --channel=conda-forge "python=3.12" "nodejs=20" pip git geckodriver firefox
mamba activate jupyter-server-proxy
```

</details>

### Python package

```bash
# Clone the repo to your local environment
git clone https://github.com/jupyterhub/jupyter-server-proxy.git
# Change directory to the jupyter-server-proxy directory
cd jupyter-server-proxy
# Install package in development mode, with the latest Jupyter clients
pip install -e ".[test,lab]"
# Link your development version of the extension with JupyterLab and Notebook
jlpm labextension develop --overwrite .
# Server extension must be manually installed in develop mode
jupyter server extension enable jupyter_server_proxy
```

## Testing

Run the tests:

```bash
pytest
```

These generate test and coverage reports in `build/pytest` and `build/coverage`.

### Acceptance tests

In `tests/acceptance`, a number of
[`.robot` files](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html)
emulate a user starting a Jupyter server, opening a real browser, clicking on
screen elements, and seeing several working proxy servers in supported Jupyter clients.

These tests are slower and more resource intensive than the unit and integration
tests, and generate additional screenshots, browser logs, server logs, and report
HTML in `build/robot`.

#### Extra browser dependencies

Compatible versions of [`geckodriver`](https://github.com/mozilla/geckodriver)
and [`firefox`](https://www.mozilla.org/en-US/firefox) need to be on `$PATH`.

These can be provisioned by [a `conda`-compatible installer](#conda), a system
package manager, or as a last resort, direct binary downloads.

#### Acceptance test dependencies

To install the additional dependencies beyond the [Python package](#python-package)
test dependencies, and run the tests against the latest Jupyter clients:

```bash
pip install -e ".[test,acceptance,lab]"
pytest
```

To run _only_ the acceptance tests, use the `-k` switch:

```bash
pytest -k acceptance
```

#### Older Jupyter Clients

To run the acceptance tests against the previous major versions of Notebook
and JupyterLab, it is advisable to use a separate, isolated environment, testing the
as-built assets from `pyproject-build`.

After creating and activating such an environment with `virtualenv` or [`conda`](#conda):

```bash
pip install --find-links ./dist/ --no-index-url jupyter-server-proxy[test,acceptance,classic]
```

## Frontend Development

To support a wide range of clients, both JupyterLab and Notebook Classic extensions
are built and distributed, each with their own quirks.

### JupyterLab/Notebook extension

The `./labextension/` directory contains the extension for the
[`lumino`](https://github.com/jupyterlab/lumino/)-based JupyterLab and Notebook
clients.

#### `nodejs`

Building this extension requires a compatible version of
[`nodejs`](https://nodejs.org/en/download/package-manager), with a supported, long
term support (LTS) release recommended.

#### `jlpm`

The `jlpm` command is a vendored, pinned version of the [`yarn`](https://yarnpkg.com)
package manager. Installed with JupyterLab, it performs commands such
as installing `npm` dependencies listed in `labextension/package.json`, building
and watching the extension from source, and formatting web-related source code files.

#### The built Lab extension

During a [`pyproject-build`](https://pypi.org/project/build/)
of the python package, a temporary JupyterLab and `jlpm` will be installed as part
of the `build-system`, executing roughly the commands:

```bash
cd labextension            # Change to the root of the labextension
jlpm                       # Install dependencies
jlpm build:prod            # Build:
                           # - `labextension/lib` with type checking
                           # - `jupyter_server_proxy/labextension` with minimization
```

During `pip install`, the built assets are copied to the user's
`{sys.prefix}/share/jupyter/labextensions/@jupyterhub/jupyter-server-proxy` to be
found by the application at startup.

#### Developing the Lab extension

For fine-grained access to the `jlpm` command and various build steps:

```bash
pip install -e .[lab]      # Ensure a compatible jlpm
cd labextension            # Change to the root of the labextension
jlpm
jlpm install:extension     # Symlink into `{sys.prefix}/share/jupyter/labextensions`
```

Watch the source directory and automatically rebuild the `labextension/lib`
and `jupyter_server_proxy/labextension` folders:

```bash
cd labextension
# Watch the source directory in one terminal, automatically rebuilding when needed
jlpm watch
# Run JupyterLab in another terminal
jupyter lab
```

While running `jlpm watch`, every saved change to a `.ts` file will immediately be
built locally and available in your running Jupyter client. "Hard" refresh JupyterLab or Notebook
with <kbd>CTRL-F5</kbd> or <kbd>⌘-F5</kbd> to load the change in your browser
(you may need to wait several seconds for the extension to be fully rebuilt).

#### Source Maps

By default, the `jlpm build` and `jlpm watch` commands generate
[source maps](https://firefox-source-docs.mozilla.org/devtools-user/debugger/how_to/use_a_source_map/)
for this extension to improve debugging using the browser development tools,
often revealed by pressing <kbd>F12</kbd>.

To also generate source maps for the JupyterLab core application, run the following command:

```bash
jupyter lab build --minimize=False
```

### Notebook Classic extension

The files in `jupyter_server_proxy/static` extend the Notebook Classic application's
_Tree_ page.

#### RequireJS

The Notebook Classic extension uses the [`require.js`](https://requirejs.org)
dependency injection system, and presently uses no dependencies beyond what is
provided by Notebook Classic.

#### The built Classic extension

During a user's `pip install`, the static assets are copied to
`{sys.prefix}/share/jupyter/nbextensions/jupyter_server_proxy`, to be
found by the application at startup.

#### Developing the Classic extension

While this extension is served as-is once installed, for live development the
extension assets must be linked:

```bash
pip install -e ".[classic]"
jupyter nbextension install --symlink --sys-prefix --py jupyter_server_proxy
```

After making changes, "hard" refresh the browser application, usually with
<kbd>CTRL-F5</kbd> or <kbd>⌘-F5</kbd>.

## Documentation

The documentation uses a fairly standard [Sphinx](https://www.sphinx-doc.org)
build chain, and requires `make` on Linux/MacOS, which cannot be installed with
`pip`

> `make` is available from [`conda-forge`](#conda) as `make` for Linux/OSX, and `m2-make`
> on Windows

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

## Linting

During continuous integration (CI) the `pre-commit` package is used to run a
number of checks, with each tool in a private virtual environment. If it is able to,
the CI bot will push to a PR with fixes.

By installing `pre-commit` with `pip` or `conda`, you can have this same experience,
or inspect the configuration to try to recreate it yourself locally.
