## [3.0]

### [3.0.0] - UNRELEASED, TODO UPDATE DATE

This release drops support for Python 3.5 and now packages the JupyterLab
extension with the Python package for use with JupyterLab 3. The JupyterLab
extension is still available on NPM for use with JupyterLab 2 but support for
JupyterLab 1 is dropped.

The Python package version jumps from 1.6.0 to 3.0.0, and the NPM package
version jumps from 2.1.2 to 3.0.0.

#### Enhancements made

* Package jupyter lab extension [#245](https://github.com/jupyterhub/jupyter-server-proxy/pull/245) ([@janjagusch](https://github.com/janjagusch))

#### Documentation improvements

* Bump to 1.6.0 (setup.py) and add CHANGELOG.md [#238](https://github.com/jupyterhub/jupyter-server-proxy/pull/238) ([@consideRatio](https://github.com/consideRatio))

#### Continuous integration

* Add publish PyPI and NPM workflow [#247](https://github.com/jupyterhub/jupyter-server-proxy/pull/247) ([@manics](https://github.com/manics))

#### Contributors to this release

[@consideRatio](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3AconsideRatio+updated%3A2021-02-08..2021-02-18&type=Issues) | [@janjagusch](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Ajanjagusch+updated%3A2021-02-08..2021-02-18&type=Issues) | [@JanJaguschQC](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3AJanJaguschQC+updated%3A2021-02-08..2021-02-18&type=Issues) | [@manics](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Amanics+updated%3A2021-02-08..2021-02-18&type=Issues) | [@yuvipanda](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Ayuvipanda+updated%3A2021-02-08..2021-02-18&type=Issues)


## [1.6]

### [1.6.0] - 2021-02-10

This release adds support for JupyterLab 3.

At this point, the Jupyterlab extension of version 2.1.2, needs to be installed
alongside the Python package for JupyterLab launcher buttons to show up as the
extension isn't yet bundled with the python package.

#### Enhancements made

* Add Jupyter Server extension data file (JupyterLab 3 support) [#235](https://github.com/jupyterhub/jupyter-server-proxy/pull/235) ([@jtpio](https://github.com/jtpio))
* Update dependencies to include jupyterlab 3.x.x (JupyterLab 3 support) [#229](https://github.com/jupyterhub/jupyter-server-proxy/pull/229) ([@dipanjank](https://github.com/dipanjank))

#### Documentation improvements

* Replace server-process list with linkable headings [#236](https://github.com/jupyterhub/jupyter-server-proxy/pull/236) ([@manics](https://github.com/manics))
* Rename the mamba-navigator example to gator in the documentation [#234](https://github.com/jupyterhub/jupyter-server-proxy/pull/234) ([@jtpio](https://github.com/jtpio))

#### Contributors to this release

[@consideRatio](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3AconsideRatio+updated%3A2021-01-05..2021-02-02&type=Issues) | [@dipanjank](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Adipanjank+updated%3A2021-01-05..2021-02-02&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Ajtpio+updated%3A2021-01-05..2021-02-02&type=Issues) | [@manics](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Amanics+updated%3A2021-01-05..2021-02-02&type=Issues) | [@yuvipanda](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Ayuvipanda+updated%3A2021-01-05..2021-02-02&type=Issues)
