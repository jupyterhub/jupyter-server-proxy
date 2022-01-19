## 3.2

### 3.2.1 - 2022-01-24

3.2.1 is a security release, fixing a vulnerability [GHSA-gcv9-6737-pjqw](https://github.com/jupyterhub/jupyter-server-proxy/security/advisories/GHSA-gcv9-6737-pjqw) where `allowed_hosts` were not validated correctly.

## Maintenance and upkeep improvements

- Modernize docs without making changes to its content [#313](https://github.com/jupyterhub/jupyter-server-proxy/pull/313) ([@consideRatio](https://github.com/consideRatio))
- Remove no longer needed logic involving six [#312](https://github.com/jupyterhub/jupyter-server-proxy/pull/312) ([@consideRatio](https://github.com/consideRatio))
- Update language, from master to main [#311](https://github.com/jupyterhub/jupyter-server-proxy/pull/311) ([@consideRatio](https://github.com/consideRatio))

## Other merged PRs

- Remove empty JupyterLab style [#314](https://github.com/jupyterhub/jupyter-server-proxy/pull/314) ([@bollwyvl](https://github.com/bollwyvl))
- ci: avoid triggering ci twice on pre-commit.ci/dependabot prs [#310](https://github.com/jupyterhub/jupyter-server-proxy/pull/310) ([@consideRatio](https://github.com/consideRatio))

## Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterhub/jupyter-server-proxy/graphs/contributors?from=2021-11-29&to=2022-01-19&type=c))

[@bollwyvl](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Abollwyvl+updated%3A2021-11-29..2022-01-19&type=Issues) | [@consideRatio](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3AconsideRatio+updated%3A2021-11-29..2022-01-19&type=Issues) | [@welcome](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Awelcome+updated%3A2021-11-29..2022-01-19&type=Issues) | [@yuvipanda](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Ayuvipanda+updated%3A2021-11-29..2022-01-19&type=Issues)


### 3.2.0 - 2021-11-29

#### New features added

- Add rewrite_response [#209](https://github.com/jupyterhub/jupyter-server-proxy/pull/209) ([@maresb](https://github.com/maresb))

#### Enhancements made

- rewrite_response hook: (HTTP status) `code` updates should sometimes automatically update `reason` [#304](https://github.com/jupyterhub/jupyter-server-proxy/pull/304) ([@maresb](https://github.com/maresb))
- Enable rewrite_response to modify status and headers [#300](https://github.com/jupyterhub/jupyter-server-proxy/pull/300) ([@ryanlovett](https://github.com/ryanlovett))
- Apply `request_headers_override` to websocket requests [#287](https://github.com/jupyterhub/jupyter-server-proxy/pull/287) ([@sk1p](https://github.com/sk1p))

#### Bugs fixed

- fix: do not follow redirects when checking if server is up [#299](https://github.com/jupyterhub/jupyter-server-proxy/pull/299) ([@ableuler](https://github.com/ableuler))
- propagate check_origin of JupyterHandler to enable CORS websocket access [#295](https://github.com/jupyterhub/jupyter-server-proxy/pull/295) ([@fhoehle](https://github.com/fhoehle))
- fix path_info for JupyterLab [#294](https://github.com/jupyterhub/jupyter-server-proxy/pull/294) ([@jhgoebbert](https://github.com/jhgoebbert))
- keep gzip-encoded content compressed [#290](https://github.com/jupyterhub/jupyter-server-proxy/pull/290) ([@axelmartenssonmodelon](https://github.com/axelmartenssonmodelon))

#### Maintenance and upkeep improvements

- resolve yarn.lock, bump builder version, some packaging metadata [#307](https://github.com/jupyterhub/jupyter-server-proxy/pull/307) ([@bollwyvl](https://github.com/bollwyvl))
- Change the rewrite_response function signature to take a RewritableResponse object [#301](https://github.com/jupyterhub/jupyter-server-proxy/pull/301) ([@maresb](https://github.com/maresb))
- Simplify wait logic for websocket connection [#292](https://github.com/jupyterhub/jupyter-server-proxy/pull/292) ([@mcg1969](https://github.com/mcg1969))

#### Documentation improvements

- Fix link to contributing.md [#291](https://github.com/jupyterhub/jupyter-server-proxy/pull/291) ([@kinow](https://github.com/kinow))

#### Continuous integration

- Test with lab [#298](https://github.com/jupyterhub/jupyter-server-proxy/pull/298) ([@maresb](https://github.com/maresb))
- Open browser not required for running pytests [#273](https://github.com/jupyterhub/jupyter-server-proxy/pull/273) ([@candlerb](https://github.com/candlerb))

#### Dependency updates

- Bump tar from 6.1.5 to 6.1.11 in /jupyterlab-server-proxy [#293](https://github.com/jupyterhub/jupyter-server-proxy/pull/293) ([@dependabot](https://github.com/dependabot))
- Bump path-parse from 1.0.6 to 1.0.7 in /jupyterlab-server-proxy [#285](https://github.com/jupyterhub/jupyter-server-proxy/pull/285) ([@dependabot](https://github.com/dependabot))
- Bump tar from 6.1.0 to 6.1.5 in /jupyterlab-server-proxy [#284](https://github.com/jupyterhub/jupyter-server-proxy/pull/284) ([@dependabot](https://github.com/dependabot))

#### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterhub/jupyter-server-proxy/graphs/contributors?from=2021-07-03&to=2021-11-29&type=c))

[@ableuler](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Aableuler+updated%3A2021-07-03..2021-11-29&type=Issues) | [@axelmartenssonmodelon](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Aaxelmartenssonmodelon+updated%3A2021-07-03..2021-11-29&type=Issues) | [@bollwyvl](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Abollwyvl+updated%3A2021-07-03..2021-11-29&type=Issues) | [@candlerb](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Acandlerb+updated%3A2021-07-03..2021-11-29&type=Issues) | [@consideRatio](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3AconsideRatio+updated%3A2021-07-03..2021-11-29&type=Issues) | [@fhoehle](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Afhoehle+updated%3A2021-07-03..2021-11-29&type=Issues) | [@jhgoebbert](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Ajhgoebbert+updated%3A2021-07-03..2021-11-29&type=Issues) | [@kinow](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Akinow+updated%3A2021-07-03..2021-11-29&type=Issues) | [@manics](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Amanics+updated%3A2021-07-03..2021-11-29&type=Issues) | [@maresb](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Amaresb+updated%3A2021-07-03..2021-11-29&type=Issues) | [@mcg1969](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Amcg1969+updated%3A2021-07-03..2021-11-29&type=Issues) | [@minrk](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Aminrk+updated%3A2021-07-03..2021-11-29&type=Issues) | [@pisymbol](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Apisymbol+updated%3A2021-07-03..2021-11-29&type=Issues) | [@ryanlovett](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Aryanlovett+updated%3A2021-07-03..2021-11-29&type=Issues) | [@sk1p](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Ask1p+updated%3A2021-07-03..2021-11-29&type=Issues) | [@yuvipanda](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Ayuvipanda+updated%3A2021-07-03..2021-11-29&type=Issues)

## 3.1

### 3.1.0 - 2021-07-02

#### New features added

- Add path_info option under launcher_entry [#279](https://github.com/jupyterhub/jupyter-server-proxy/pull/279) ([@ryanlovett](https://github.com/ryanlovett))
- Add request_headers_override configuration [#252](https://github.com/jupyterhub/jupyter-server-proxy/pull/252) ([@ryanlovett](https://github.com/ryanlovett))

#### Bugs fixed

- More precise regexp matching for /proxy/absolute/<host>:<port> [#271](https://github.com/jupyterhub/jupyter-server-proxy/pull/271) ([@candlerb](https://github.com/candlerb))

#### Maintenance and upkeep improvements

- Reduce (and test) sdist size [#263](https://github.com/jupyterhub/jupyter-server-proxy/pull/263) ([@bollwyvl](https://github.com/bollwyvl))

#### Continuous integration

- Add acceptance testing with robotframework(-jupyterlibrary) [#269](https://github.com/jupyterhub/jupyter-server-proxy/pull/269) ([@bollwyvl](https://github.com/bollwyvl))

#### #### Dependency updates

- Bump postcss from 7.0.35 to 7.0.36 in /jupyterlab-server-proxy [#277](https://github.com/jupyterhub/jupyter-server-proxy/pull/277) ([@dependabot](https://github.com/dependabot))
- Bump normalize-url from 4.5.0 to 4.5.1 in /jupyterlab-server-proxy [#276](https://github.com/jupyterhub/jupyter-server-proxy/pull/276) ([@dependabot](https://github.com/dependabot))
- Bump ws from 7.4.4 to 7.4.6 in /jupyterlab-server-proxy [#275](https://github.com/jupyterhub/jupyter-server-proxy/pull/275) ([@dependabot](https://github.com/dependabot))
- Bump browserslist from 4.16.3 to 4.16.6 in /jupyterlab-server-proxy [#274](https://github.com/jupyterhub/jupyter-server-proxy/pull/274) ([@dependabot](https://github.com/dependabot))

#### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterhub/jupyter-server-proxy/graphs/contributors?from=2021-03-16&to=2021-07-03&type=c))

[@bollwyvl](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Abollwyvl+updated%3A2021-03-16..2021-07-03&type=Issues) | [@candlerb](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Acandlerb+updated%3A2021-03-16..2021-07-03&type=Issues) | [@jhgoebbert](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Ajhgoebbert+updated%3A2021-03-16..2021-07-03&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Ajtpio+updated%3A2021-03-16..2021-07-03&type=Issues) | [@manics](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Amanics+updated%3A2021-03-16..2021-07-03&type=Issues) | [@ryanlovett](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Aryanlovett+updated%3A2021-03-16..2021-07-03&type=Issues) | [@yuvipanda](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Ayuvipanda+updated%3A2021-03-16..2021-07-03&type=Issues)

## 3.0

### 3.0.2 - 2020-03-16

#### Bugs fixed

* Include jupyterlab-server-proxy in the sdist [#260](https://github.com/jupyterhub/jupyter-server-proxy/pull/260) ([@xhochy](https://github.com/xhochy))

#### Contributors to this release

[@xhochy](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Axhochy+updated%3A2021-03-16..2021-03-16&type=Issues)

### 3.0.1 - 2020-03-16

#### Bugs fixed

* Fix PyPI url [#259](https://github.com/jupyterhub/jupyter-server-proxy/pull/259) ([@janjagusch](https://github.com/janjagusch))

#### Contributors to this release

[@janjagusch](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Ajanjagusch+updated%3A2021-03-15..2021-03-16&type=Issues)

### 3.0.0 - 2020-03-15

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

## 1.6

### 1.6.0 - 2021-02-10

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
