## [3.0]

### [3.0.2] - 2020-03-16

## Bugs fixed

* Include jupyterlab-server-proxy in the sdist [#260](https://github.com/jupyterhub/jupyter-server-proxy/pull/260) ([@xhochy](https://github.com/xhochy))

## Contributors to this release

[@xhochy](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Axhochy+updated%3A2021-03-16..2021-03-16&type=Issues)

### [3.0.1] - 2020-03-16

#### Bugs fixed

* Fix PyPI url [#259](https://github.com/jupyterhub/jupyter-server-proxy/pull/259) ([@janjagusch](https://github.com/janjagusch))

#### Contributors to this release

[@janjagusch](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Ajanjagusch+updated%3A2021-03-15..2021-03-16&type=Issues)

### [3.0.0] - 2020-03-15

This release drops support for Python 3.5 and now packages the JupyterLab
extension with the Python package for use with JupyterLab 3. The JupyterLab
extension is still available on NPM for use with JupyterLab 2 but support for
JupyterLab 1 is dropped.

The Python package version jumps from 1.6.0 to 3.0.0, and the NPM package
version jumps from 2.1.2 to 3.0.0.

#### Enhancements made

* Package jupyter lab extension [#245](https://github.com/jupyterhub/jupyter-server-proxy/pull/245) ([@janjagusch](https://github.com/janjagusch))

#### Maintenance and upkeep improvements

* Breaking: Replace host_whitelist with host_allowlist [#256](https://github.com/jupyterhub/jupyter-server-proxy/pull/256) ([@manics](https://github.com/manics))
* Switch from notebook to jupyter-server [#254](https://github.com/jupyterhub/jupyter-server-proxy/pull/254) ([@manics](https://github.com/manics))

#### Continuous integration

* Move build.yaml into test.yaml [#255](https://github.com/jupyterhub/jupyter-server-proxy/pull/255) ([@manics](https://github.com/manics))
* Fix build.yaml workflow [#249](https://github.com/jupyterhub/jupyter-server-proxy/pull/249) ([@manics](https://github.com/manics))
* Add publish PyPI and NPM workflow [#247](https://github.com/jupyterhub/jupyter-server-proxy/pull/247) ([@manics](https://github.com/manics))
* tests: remove bad test, add new clarifying current behavior [#240](https://github.com/jupyterhub/jupyter-server-proxy/pull/240) ([@consideRatio](https://github.com/consideRatio))

#### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterhub/jupyter-server-proxy/graphs/contributors?from=2021-02-08&to=2021-03-15&type=c))

[@AlJohri](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3AAlJohri+updated%3A2021-02-08..2021-03-15&type=Issues) | [@consideRatio](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3AconsideRatio+updated%3A2021-02-08..2021-03-15&type=Issues) | [@ian-r-rose](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Aian-r-rose+updated%3A2021-02-08..2021-03-15&type=Issues) | [@janjagusch](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Ajanjagusch+updated%3A2021-02-08..2021-03-15&type=Issues) | [@JanJaguschQC](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3AJanJaguschQC+updated%3A2021-02-08..2021-03-15&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Ajtpio+updated%3A2021-02-08..2021-03-15&type=Issues) | [@manics](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Amanics+updated%3A2021-02-08..2021-03-15&type=Issues) | [@maresb](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Amaresb+updated%3A2021-02-08..2021-03-15&type=Issues) | [@minrk](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Aminrk+updated%3A2021-02-08..2021-03-15&type=Issues) | [@ryanlovett](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Aryanlovett+updated%3A2021-02-08..2021-03-15&type=Issues) | [@todo](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Atodo+updated%3A2021-02-08..2021-03-15&type=Issues) | [@yuvipanda](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Ayuvipanda+updated%3A2021-02-08..2021-03-15&type=Issues)

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

* Bump to 1.6.0 (setup.py) and add CHANGELOG.md [#238](https://github.com/jupyterhub/jupyter-server-proxy/pull/238) ([@consideRatio](https://github.com/consideRatio))
* Replace server-process list with linkable headings [#236](https://github.com/jupyterhub/jupyter-server-proxy/pull/236) ([@manics](https://github.com/manics))
* Rename the mamba-navigator example to gator in the documentation [#234](https://github.com/jupyterhub/jupyter-server-proxy/pull/234) ([@jtpio](https://github.com/jtpio))

#### Contributors to this release

[@consideRatio](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3AconsideRatio+updated%3A2021-02-08..2021-02-25&type=Issues) | [@janjagusch](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Ajanjagusch+updated%3A2021-02-08..2021-02-25&type=Issues) | [@JanJaguschQC](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3AJanJaguschQC+updated%3A2021-02-08..2021-02-25&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Ajtpio+updated%3A2021-02-08..2021-02-25&type=Issues) | [@manics](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Amanics+updated%3A2021-02-08..2021-02-25&type=Issues) | [@ryanlovett](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Aryanlovett+updated%3A2021-02-08..2021-02-25&type=Issues) | [@yuvipanda](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Ayuvipanda+updated%3A2021-02-08..2021-02-25&type=Issues)
