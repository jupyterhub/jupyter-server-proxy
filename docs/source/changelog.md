# Changelog

## 4.3

### v4.3.0 - 2024-07-01

#### New features added

- feat: Allow Skipping of Activity Reporting [#473](https://github.com/jupyterhub/jupyter-server-proxy/pull/473) ([@sdmichelini](https://github.com/sdmichelini), [@yuvipanda](https://github.com/yuvipanda), [@ryanlovett](https://github.com/ryanlovett), [@deser](https://github.com/deser))
- Allow configuring jupyterlab launcher category [#453](https://github.com/jupyterhub/jupyter-server-proxy/pull/453) ([@dylex](https://github.com/dylex), [@yuvipanda](https://github.com/yuvipanda), [@bollwyvl](https://github.com/bollwyvl), [@imcovangent](https://github.com/imcovangent))
- Add `raw_socket_proxy` to directly proxy websockets to TCP/unix sockets [#447](https://github.com/jupyterhub/jupyter-server-proxy/pull/447) ([@dylex](https://github.com/dylex), [@yuvipanda](https://github.com/yuvipanda), [@manics](https://github.com/manics))

#### Bugs fixed

- Fix failure to update \_\_version\_\_ [#481](https://github.com/jupyterhub/jupyter-server-proxy/pull/481) ([@consideRatio](https://github.com/consideRatio))
- Prevent failed entrypoints from spoiling the launch [#443](https://github.com/jupyterhub/jupyter-server-proxy/pull/443) ([@banesullivan-kobold](https://github.com/banesullivan-kobold), [@yuvipanda](https://github.com/yuvipanda))

#### Documentation improvements

- Detail fixes in RELEASE.md [#487](https://github.com/jupyterhub/jupyter-server-proxy/pull/487) ([@consideRatio](https://github.com/consideRatio))
- Fixed jlpm to jupyter in bash command [#478](https://github.com/jupyterhub/jupyter-server-proxy/pull/478) ([@imcovangent](https://github.com/imcovangent), [@yuvipanda](https://github.com/yuvipanda))

#### Continuous integration improvements

- ci: remove workaround running test in py311 instead of py312 [#485](https://github.com/jupyterhub/jupyter-server-proxy/pull/485) ([@consideRatio](https://github.com/consideRatio))
- ci: reference node lts to avoid need to bump in october [#484](https://github.com/jupyterhub/jupyter-server-proxy/pull/484) ([@consideRatio](https://github.com/consideRatio))
- ci: fix test failure on windows and error on bash pipe failures etc [#483](https://github.com/jupyterhub/jupyter-server-proxy/pull/483) ([@consideRatio](https://github.com/consideRatio))

#### Contributors to this release

The following people contributed discussions, new ideas, code and documentation contributions, and review.
See [our definition of contributors](https://github-activity.readthedocs.io/en/latest/#how-does-this-tool-define-contributions-in-the-reports).

([GitHub contributors page for this release](https://github.com/jupyterhub/jupyter-server-proxy/graphs/contributors?from=2024-06-11&to=2024-07-01&type=c))

@banesullivan-kobold ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Abanesullivan-kobold+updated%3A2024-06-11..2024-07-01&type=Issues)) | @bollwyvl ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Abollwyvl+updated%3A2024-06-11..2024-07-01&type=Issues)) | @consideRatio ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3AconsideRatio+updated%3A2024-06-11..2024-07-01&type=Issues)) | @costa ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Acosta+updated%3A2024-06-11..2024-07-01&type=Issues)) | @deser ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Adeser+updated%3A2024-06-11..2024-07-01&type=Issues)) | @dylex ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Adylex+updated%3A2024-06-11..2024-07-01&type=Issues)) | @imcovangent ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Aimcovangent+updated%3A2024-06-11..2024-07-01&type=Issues)) | @manics ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Amanics+updated%3A2024-06-11..2024-07-01&type=Issues)) | @ryanlovett ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Aryanlovett+updated%3A2024-06-11..2024-07-01&type=Issues)) | @sdmichelini ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Asdmichelini+updated%3A2024-06-11..2024-07-01&type=Issues)) | @yuvipanda ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Ayuvipanda+updated%3A2024-06-11..2024-07-01&type=Issues))

## 4.2

### v4.2.0 - 2024-06-11

This release includes an important security patch for
[CVE-2024-35225 ](https://github.com/jupyterhub/jupyter-server-proxy/security/advisories/GHSA-fvcq-4x64-hqxr).

([full changelog](https://github.com/jupyterhub/jupyter-server-proxy/compare/v4.1.2...v4.2.0))

#### Maintenance and upkeep improvements

- Require jupyter_server 1.24+, tornado 6.1+, traitlets 5.1+ [#467](https://github.com/jupyterhub/jupyter-server-proxy/pull/467) ([@consideRatio](https://github.com/consideRatio))
- Test against Python 3.12 [#450](https://github.com/jupyterhub/jupyter-server-proxy/pull/450) ([@consideRatio](https://github.com/consideRatio))

#### Documentation improvements

- Document the correct default value for new_browser_tab. [#470](https://github.com/jupyterhub/jupyter-server-proxy/pull/470) ([@ryanlovett](https://github.com/ryanlovett))

#### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterhub/jupyter-server-proxy/graphs/contributors?from=2024-03-19&to=2024-06-08&type=c))

[@consideRatio](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3AconsideRatio+updated%3A2024-03-19..2024-06-08&type=Issues) | [@ryanlovett](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Aryanlovett+updated%3A2024-03-19..2024-06-08&type=Issues) | [@welcome](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Awelcome+updated%3A2024-03-19..2024-06-08&type=Issues)

## 4.1

### 4.1.2 - 2024-03-13

#### Bugs fixed

- Keep proxying all requested subprotocols [#462](https://github.com/jupyterhub/jupyter-server-proxy/pull/462) ([@consideRatio](https://github.com/consideRatio))

### 4.1.1 - 2024-03-13

This release includes an important security patch for the critical vulnerability
[GHSA-w3vc-fx9p-wp4v](https://github.com/jupyterhub/jupyter-server-proxy/security/advisories/GHSA-w3vc-fx9p-wp4v).
The security patch is also available in version 3.2.3.

#### Bugs fixed

- Ensure no blank `Sec-Websocket-Protocol` headers and warn if websocket subprotocol edge case occur [#458](https://github.com/jupyterhub/jupyter-server-proxy/pull/458) ([@consideRatio](https://github.com/consideRatio), [@duytnguyendtn](https://github.com/duytnguyendtn), [@minrk](https://github.com/minrk), [@benz0li](https://github.com/benz0li))
- Fix double formatting of callables (`command`, `environment`, `request_headers_override`) [#437](https://github.com/jupyterhub/jupyter-server-proxy/pull/437) ([@diocas](https://github.com/diocas), [@consideRatio](https://github.com/consideRatio))

#### Maintenance and upkeep improvements

- labextension: refreeze yarn.lock [#461](https://github.com/jupyterhub/jupyter-server-proxy/pull/461) ([@consideRatio](https://github.com/consideRatio))
- List tornado and traitlets as dependencies explicitly, and cleanup unreachable code [#457](https://github.com/jupyterhub/jupyter-server-proxy/pull/457) ([@consideRatio](https://github.com/consideRatio), [@minrk](https://github.com/minrk))
- Fix failure to upload code coverage reports [#454](https://github.com/jupyterhub/jupyter-server-proxy/pull/454) ([@consideRatio](https://github.com/consideRatio))
- Update tests for notebook 7.1 [#451](https://github.com/jupyterhub/jupyter-server-proxy/pull/451) ([@consideRatio](https://github.com/consideRatio))
- tests: fix failure to log error after all retries failed [#441](https://github.com/jupyterhub/jupyter-server-proxy/pull/441) ([@consideRatio](https://github.com/consideRatio))
- Declare metadata in pyproject.toml, remove hatch-nodejs-version plugin [#427](https://github.com/jupyterhub/jupyter-server-proxy/pull/427) ([@consideRatio](https://github.com/consideRatio), [@bollwyvl](https://github.com/bollwyvl), [@manics](https://github.com/manics))

#### Continuous integration improvements

- ci: upgrade to v4 of upload/download-artifact actions [#455](https://github.com/jupyterhub/jupyter-server-proxy/pull/455) ([@consideRatio](https://github.com/consideRatio))
- ci: schedule test runs twice a week [#452](https://github.com/jupyterhub/jupyter-server-proxy/pull/452) ([@consideRatio](https://github.com/consideRatio))

#### Contributors to this release

The following people contributed discussions, new ideas, code and documentation contributions, and review.
See [our definition of contributors](https://github-activity.readthedocs.io/en/latest/#how-does-this-tool-define-contributions-in-the-reports).

([GitHub contributors page for this release](https://github.com/jupyterhub/jupyter-server-proxy/graphs/contributors?from=2023-09-25&to=2024-03-13&type=c))

@benz0li ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Abenz0li+updated%3A2023-09-25..2024-03-13&type=Issues)) | @bollwyvl ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Abollwyvl+updated%3A2023-09-25..2024-03-13&type=Issues)) | @consideRatio ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3AconsideRatio+updated%3A2023-09-25..2024-03-13&type=Issues)) | @diocas ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Adiocas+updated%3A2023-09-25..2024-03-13&type=Issues)) | @duytnguyendtn ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Aduytnguyendtn+updated%3A2023-09-25..2024-03-13&type=Issues)) | @goekce ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Agoekce+updated%3A2023-09-25..2024-03-13&type=Issues)) | @manics ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Amanics+updated%3A2023-09-25..2024-03-13&type=Issues)) | @minrk ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Aminrk+updated%3A2023-09-25..2024-03-13&type=Issues)) | @rcthomas ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Arcthomas+updated%3A2023-09-25..2024-03-13&type=Issues)) | @sk1p ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Ask1p+updated%3A2023-09-25..2024-03-13&type=Issues)) | @steverweber ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Asteverweber+updated%3A2023-09-25..2024-03-13&type=Issues)) | @yuvipanda ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Ayuvipanda+updated%3A2023-09-25..2024-03-13&type=Issues))

### 4.1.0 - 2023-09-25

#### New features added

- Add extension for Jupyter Notebook 7 [#425](https://github.com/jupyterhub/jupyter-server-proxy/pull/425) ([@bollwyvl](https://github.com/bollwyvl), [@consideRatio](https://github.com/consideRatio))
- Add JupyterLab 4 support for the extension [#419](https://github.com/jupyterhub/jupyter-server-proxy/pull/419) ([@trungleduc](https://github.com/trungleduc), [@consideRatio](https://github.com/consideRatio), [@manics](https://github.com/manics), [@bollwyvl](https://github.com/bollwyvl), [@ryanlovett](https://github.com/ryanlovett), [@Khagesh16](https://github.com/Khagesh16))

#### Bugs fixed

- Ensure proxying to Unix sockets constructs separate HTTP clients [#415](https://github.com/jupyterhub/jupyter-server-proxy/pull/415) ([@takluyver](https://github.com/takluyver), [@manics](https://github.com/manics))

#### Continuous integration improvements

- Work around incompatibility (missing firefox_profile arg) for acceptance tests [#416](https://github.com/jupyterhub/jupyter-server-proxy/pull/416) ([@takluyver](https://github.com/takluyver), [@manics](https://github.com/manics))
- ci: cleanup stashed SHA256 checksum before publish to PyPI [#401](https://github.com/jupyterhub/jupyter-server-proxy/pull/401) ([@consideRatio](https://github.com/consideRatio))
- Test Windows [#392](https://github.com/jupyterhub/jupyter-server-proxy/pull/392) ([@manics](https://github.com/manics), [@consideRatio](https://github.com/consideRatio), [@bollwyvl](https://github.com/bollwyvl))

#### Dependency updates

- labextension: refreeze yarn.lock [#422](https://github.com/jupyterhub/jupyter-server-proxy/pull/422) ([@consideRatio](https://github.com/consideRatio))
- labextension: refreeze yarn.lock [#400](https://github.com/jupyterhub/jupyter-server-proxy/pull/400) ([@consideRatio](https://github.com/consideRatio))

#### Contributors to this release

The following people contributed discussions, new ideas, code and documentation contributions, and review.
See [our definition of contributors](https://github-activity.readthedocs.io/en/latest/#how-does-this-tool-define-contributions-in-the-reports).

([GitHub contributors page for this release](https://github.com/jupyterhub/jupyter-server-proxy/graphs/contributors?from=2023-04-20&to=2023-09-25&type=c))

@bollwyvl ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Abollwyvl+updated%3A2023-04-20..2023-09-25&type=Issues)) | @cataluna84 ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Acataluna84+updated%3A2023-04-20..2023-09-25&type=Issues)) | @consideRatio ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3AconsideRatio+updated%3A2023-04-20..2023-09-25&type=Issues)) | @Khagesh16 ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3AKhagesh16+updated%3A2023-04-20..2023-09-25&type=Issues)) | @manics ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Amanics+updated%3A2023-04-20..2023-09-25&type=Issues)) | @oeway ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Aoeway+updated%3A2023-04-20..2023-09-25&type=Issues)) | @ryanlovett ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Aryanlovett+updated%3A2023-04-20..2023-09-25&type=Issues)) | @takluyver ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Atakluyver+updated%3A2023-04-20..2023-09-25&type=Issues)) | @trungleduc ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Atrungleduc+updated%3A2023-04-20..2023-09-25&type=Issues))

## 4.0

### 4.0.0 - 2023-04-20

#### Breaking changes

- jupyter-server-proxy now requires Python 3.8+ ([#350](https://github.com/jupyterhub/jupyter-server-proxy/pull/350), [#387](https://github.com/jupyterhub/jupyter-server-proxy/pull/387))
- jupyter-server-proxy's JupyterLab extension dropped support for JupyterLab 2 ([#394](https://github.com/jupyterhub/jupyter-server-proxy/pull/394))
- jupyter-server-proxy's JupyterLab extension renamed from @jupyterlab/server-proxy to @jupyterhub/jupyter-server-proxy ([#368](https://github.com/jupyterhub/jupyter-server-proxy/pull/368))

#### New features added

- Accept an unset `command` to proxy to an already started process (unmanaged process) [#339](https://github.com/jupyterhub/jupyter-server-proxy/pull/339) ([@ryshoooo](https://github.com/ryshoooo))
- Support proxying to a server process via a Unix socket [#337](https://github.com/jupyterhub/jupyter-server-proxy/pull/337) ([@takluyver](https://github.com/takluyver))

#### Bugs fixed

- Use `pytest.fixture`s for starting servers, use `importlib*metadata` [#396](https://github.com/jupyterhub/jupyter-server-proxy/pull/396) ([@bollwyvl](https://github.com/bollwyvl))

#### Maintenance and upkeep improvements

- maint: update package description to not claim windows support [#398](https://github.com/jupyterhub/jupyter-server-proxy/pull/398) ([@consideRatio](https://github.com/consideRatio))
- Use `pytest.fixture`s for starting servers, use `importlib*metadata` [#396](https://github.com/jupyterhub/jupyter-server-proxy/pull/396) ([@bollwyvl](https://github.com/bollwyvl))
- maint, breaking: drop support for jupyterlab 2 [#394](https://github.com/jupyterhub/jupyter-server-proxy/pull/394) ([@consideRatio](https://github.com/consideRatio))
- Fix editable install and update CONTRIBUTING.md [#391](https://github.com/jupyterhub/jupyter-server-proxy/pull/391) ([@mahendrapaipuri](https://github.com/mahendrapaipuri))
- pre-commit: add config and small fixes [#390](https://github.com/jupyterhub/jupyter-server-proxy/pull/390) ([@consideRatio](https://github.com/consideRatio))
- Drop support for Python 3.7 [#387](https://github.com/jupyterhub/jupyter-server-proxy/pull/387) ([@consideRatio](https://github.com/consideRatio))
- dependabot: monthly updates of github actions [#385](https://github.com/jupyterhub/jupyter-server-proxy/pull/385) ([@consideRatio](https://github.com/consideRatio))
- Adopt hatchling, plugins for python package build [#371](https://github.com/jupyterhub/jupyter-server-proxy/pull/371) ([@bollwyvl](https://github.com/bollwyvl))
- Rename @jupyterlab/server-proxy to @jupyterhub/jupyter-server-proxy [#368](https://github.com/jupyterhub/jupyter-server-proxy/pull/368) ([@consideRatio](https://github.com/consideRatio))
- Update labextension build [#355](https://github.com/jupyterhub/jupyter-server-proxy/pull/355) ([@bollwyvl](https://github.com/bollwyvl))
- Refine RELEASE.md with tbump [#353](https://github.com/jupyterhub/jupyter-server-proxy/pull/353) ([@consideRatio](https://github.com/consideRatio))
- Drop support for Python 3.6 [#350](https://github.com/jupyterhub/jupyter-server-proxy/pull/350) ([@consideRatio](https://github.com/consideRatio))

#### Documentation improvements

- docs: convert .rst to MyST based markdown files [#393](https://github.com/jupyterhub/jupyter-server-proxy/pull/393) ([@consideRatio](https://github.com/consideRatio))
- Fix imshields link README.md [#375](https://github.com/jupyterhub/jupyter-server-proxy/pull/375) ([@prabhakk-mw](https://github.com/prabhakk-mw))
- docs: remove outdated release docs in favor of RELEASE.md [#369](https://github.com/jupyterhub/jupyter-server-proxy/pull/369) ([@consideRatio](https://github.com/consideRatio))
- README: warn about unlimited local network access [#359](https://github.com/jupyterhub/jupyter-server-proxy/pull/359) ([@manics](https://github.com/manics))
- docs: switch from alabaster to sphinx-book-theme, and misc docs build system maintenance [#352](https://github.com/jupyterhub/jupyter-server-proxy/pull/352) ([@consideRatio](https://github.com/consideRatio))
- Fix config filename in config via traitlets doc [#344](https://github.com/jupyterhub/jupyter-server-proxy/pull/344) ([@cmd-ntrf](https://github.com/cmd-ntrf))

#### Continuous integration improvements

- Fix tests against jupyter_server 2 [#366](https://github.com/jupyterhub/jupyter-server-proxy/pull/366) ([@bollwyvl](https://github.com/bollwyvl))
- ci: use ubuntu-22.04, firefox and geckodriver now available [#364](https://github.com/jupyterhub/jupyter-server-proxy/pull/364) ([@consideRatio](https://github.com/consideRatio))
- ci: update github actions, small refactors, add dependabot for gha [#351](https://github.com/jupyterhub/jupyter-server-proxy/pull/351) ([@consideRatio](https://github.com/consideRatio))
- ci: test against modern python versions and fix broken test suite [#348](https://github.com/jupyterhub/jupyter-server-proxy/pull/348) ([@consideRatio](https://github.com/consideRatio))

#### Dependency updates

- build(deps): bump webpack from 5.75.0 to 5.76.1 in /labextension [#380](https://github.com/jupyterhub/jupyter-server-proxy/pull/380) ([@dependabot](https://github.com/dependabot))
- build(deps): bump http-cache-semantics from 4.1.0 to 4.1.1 in /labextension [#376](https://github.com/jupyterhub/jupyter-server-proxy/pull/376) ([@dependabot](https://github.com/dependabot))
- build(deps): bump json5 from 2.2.1 to 2.2.2 in /jupyterlab-server-proxy [#365](https://github.com/jupyterhub/jupyter-server-proxy/pull/365) ([@dependabot](https://github.com/dependabot))
- build(deps): bump loader-utils from 3.2.0 to 3.2.1 in /jupyterlab-server-proxy [#357](https://github.com/jupyterhub/jupyter-server-proxy/pull/357) ([@dependabot](https://github.com/dependabot))

#### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterhub/jupyter-server-proxy/graphs/contributors?from=2022-09-08&to=2023-04-18&type=c))

[@bollwyvl](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Abollwyvl+updated%3A2022-09-08..2023-04-18&type=Issues) | [@choldgraf](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Acholdgraf+updated%3A2022-09-08..2023-04-18&type=Issues) | [@cmd-ntrf](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Acmd-ntrf+updated%3A2022-09-08..2023-04-18&type=Issues) | [@consideRatio](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3AconsideRatio+updated%3A2022-09-08..2023-04-18&type=Issues) | [@dependabot](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Adependabot+updated%3A2022-09-08..2023-04-18&type=Issues) | [@ellisonbg](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Aellisonbg+updated%3A2022-09-08..2023-04-18&type=Issues) | [@Finesim97](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3AFinesim97+updated%3A2022-09-08..2023-04-18&type=Issues) | [@jhgoebbert](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Ajhgoebbert+updated%3A2022-09-08..2023-04-18&type=Issues) | [@mahendrapaipuri](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Amahendrapaipuri+updated%3A2022-09-08..2023-04-18&type=Issues) | [@manics](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Amanics+updated%3A2022-09-08..2023-04-18&type=Issues) | [@prabhakk-mw](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Aprabhakk-mw+updated%3A2022-09-08..2023-04-18&type=Issues) | [@ryanlovett](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Aryanlovett+updated%3A2022-09-08..2023-04-18&type=Issues) | [@ryshoooo](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Aryshoooo+updated%3A2022-09-08..2023-04-18&type=Issues) | [@takluyver](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Atakluyver+updated%3A2022-09-08..2023-04-18&type=Issues) | [@yuvipanda](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Ayuvipanda+updated%3A2022-09-08..2023-04-18&type=Issues)

## 3.2

### 3.2.3 - 2024-03-13

This is a security release for [GHSA-w3vc-fx9p-wp4v](https://github.com/jupyterhub/jupyter-server-proxy/security/advisories/GHSA-w3vc-fx9p-wp4v).

### 3.2.2 - 2022-09-08

#### Bugs fixed

- add allow-downloads and allow-modals to sandbox [#335](https://github.com/jupyterhub/jupyter-server-proxy/pull/335) ([@djangoliv](https://github.com/djangoliv))
- allow empty PUT body [#331](https://github.com/jupyterhub/jupyter-server-proxy/pull/331) ([@pepijndevos](https://github.com/pepijndevos))
- [bugfix] Hop by hop header handling [#328](https://github.com/jupyterhub/jupyter-server-proxy/pull/328) ([@mahnerak](https://github.com/mahnerak))

#### Documentation improvements

- Yarn link malformed. [#320](https://github.com/jupyterhub/jupyter-server-proxy/pull/320) ([@matthew-brett](https://github.com/matthew-brett))

#### Continuous integration improvements

- Install `notebook<7` for notebook test [#340](https://github.com/jupyterhub/jupyter-server-proxy/pull/340) ([@manics](https://github.com/manics))
- Run publish workflow for tags [#318](https://github.com/jupyterhub/jupyter-server-proxy/pull/318) ([@manics](https://github.com/manics))

#### Dependency updates

- Bump terser from 5.10.0 to 5.14.2 in /jupyterlab-server-proxy [#342](https://github.com/jupyterhub/jupyter-server-proxy/pull/342) ([@dependabot](https://github.com/dependabot))
- Bump moment from 2.29.2 to 2.29.4 in /jupyterlab-server-proxy [#341](https://github.com/jupyterhub/jupyter-server-proxy/pull/341) ([@dependabot](https://github.com/dependabot))
- Bump moment from 2.29.1 to 2.29.2 in /jupyterlab-server-proxy [#336](https://github.com/jupyterhub/jupyter-server-proxy/pull/336) ([@dependabot](https://github.com/dependabot))
- Bump minimist from 1.2.5 to 1.2.6 in /jupyterlab-server-proxy [#334](https://github.com/jupyterhub/jupyter-server-proxy/pull/334) ([@dependabot](https://github.com/dependabot))
- Bump url-parse from 1.5.3 to 1.5.7 in /jupyterlab-server-proxy [#327](https://github.com/jupyterhub/jupyter-server-proxy/pull/327) ([@dependabot](https://github.com/dependabot))

#### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterhub/jupyter-server-proxy/graphs/contributors?from=2022-01-24&to=2022-09-08&type=c))

[@austinmw](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Aaustinmw+updated%3A2022-01-24..2022-09-08&type=Issues) | [@bollwyvl](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Abollwyvl+updated%3A2022-01-24..2022-09-08&type=Issues) | [@consideRatio](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3AconsideRatio+updated%3A2022-01-24..2022-09-08&type=Issues) | [@dependabot](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Adependabot+updated%3A2022-01-24..2022-09-08&type=Issues) | [@djangoliv](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Adjangoliv+updated%3A2022-01-24..2022-09-08&type=Issues) | [@jhgoebbert](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Ajhgoebbert+updated%3A2022-01-24..2022-09-08&type=Issues) | [@mahnerak](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Amahnerak+updated%3A2022-01-24..2022-09-08&type=Issues) | [@manics](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Amanics+updated%3A2022-01-24..2022-09-08&type=Issues) | [@matthew-brett](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Amatthew-brett+updated%3A2022-01-24..2022-09-08&type=Issues) | [@meeseeksmachine](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Ameeseeksmachine+updated%3A2022-01-24..2022-09-08&type=Issues) | [@pepijndevos](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Apepijndevos+updated%3A2022-01-24..2022-09-08&type=Issues) | [@ryanlovett](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Aryanlovett+updated%3A2022-01-24..2022-09-08&type=Issues) | [@ryshoooo](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Aryshoooo+updated%3A2022-01-24..2022-09-08&type=Issues) | [@takluyver](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Atakluyver+updated%3A2022-01-24..2022-09-08&type=Issues) | [@yuvipanda](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Ayuvipanda+updated%3A2022-01-24..2022-09-08&type=Issues)

### 3.2.1 - 2022-01-24

3.2.1 is a security release, fixing a vulnerability [GHSA-gcv9-6737-pjqw](https://github.com/jupyterhub/jupyter-server-proxy/security/advisories/GHSA-gcv9-6737-pjqw) where `allowed_hosts` were not validated correctly.

#### Maintenance and upkeep improvements

- Remove empty JupyterLab style [#314](https://github.com/jupyterhub/jupyter-server-proxy/pull/314) ([@bollwyvl](https://github.com/bollwyvl))
- Modernize docs without making changes to its content [#313](https://github.com/jupyterhub/jupyter-server-proxy/pull/313) ([@consideRatio](https://github.com/consideRatio))
- Remove no longer needed logic involving six [#312](https://github.com/jupyterhub/jupyter-server-proxy/pull/312) ([@consideRatio](https://github.com/consideRatio))
- Update language, from master to main [#311](https://github.com/jupyterhub/jupyter-server-proxy/pull/311) ([@consideRatio](https://github.com/consideRatio))

#### Continuous integration improvements

- ci: avoid triggering ci twice on pre-commit.ci/dependabot prs [#310](https://github.com/jupyterhub/jupyter-server-proxy/pull/310) ([@consideRatio](https://github.com/consideRatio))

#### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterhub/jupyter-server-proxy/graphs/contributors?from=2021-11-29&to=2022-01-19&type=c))

[@bollwyvl](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Abollwyvl+updated%3A2021-11-29..2022-01-19&type=Issues) | [@consideRatio](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3AconsideRatio+updated%3A2021-11-29..2022-01-19&type=Issues) | [@yuvipanda](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Ayuvipanda+updated%3A2021-11-29..2022-01-19&type=Issues)

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

#### Continuous integration improvements

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

#### Continuous integration improvements

- Add acceptance testing with robotframework(-jupyterlibrary) [#269](https://github.com/jupyterhub/jupyter-server-proxy/pull/269) ([@bollwyvl](https://github.com/bollwyvl))

#### Dependency updates

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

- Include jupyterlab-server-proxy in the sdist [#260](https://github.com/jupyterhub/jupyter-server-proxy/pull/260) ([@xhochy](https://github.com/xhochy))

#### Contributors to this release

[@xhochy](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Axhochy+updated%3A2021-03-16..2021-03-16&type=Issues)

### 3.0.1 - 2020-03-16

#### Bugs fixed

- Fix PyPI url [#259](https://github.com/jupyterhub/jupyter-server-proxy/pull/259) ([@janjagusch](https://github.com/janjagusch))

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

- Package jupyter lab extension [#245](https://github.com/jupyterhub/jupyter-server-proxy/pull/245) ([@janjagusch](https://github.com/janjagusch))

#### Maintenance and upkeep improvements

- Breaking: Replace host_whitelist with host_allowlist [#256](https://github.com/jupyterhub/jupyter-server-proxy/pull/256) ([@manics](https://github.com/manics))
- Switch from notebook to jupyter-server [#254](https://github.com/jupyterhub/jupyter-server-proxy/pull/254) ([@manics](https://github.com/manics))

#### Continuous integration improvements

- Move build.yaml into test.yaml [#255](https://github.com/jupyterhub/jupyter-server-proxy/pull/255) ([@manics](https://github.com/manics))
- Fix build.yaml workflow [#249](https://github.com/jupyterhub/jupyter-server-proxy/pull/249) ([@manics](https://github.com/manics))
- Add publish PyPI and NPM workflow [#247](https://github.com/jupyterhub/jupyter-server-proxy/pull/247) ([@manics](https://github.com/manics))
- tests: remove bad test, add new clarifying current behavior [#240](https://github.com/jupyterhub/jupyter-server-proxy/pull/240) ([@consideRatio](https://github.com/consideRatio))

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

- Add Jupyter Server extension data file (JupyterLab 3 support) [#235](https://github.com/jupyterhub/jupyter-server-proxy/pull/235) ([@jtpio](https://github.com/jtpio))
- Update dependencies to include jupyterlab 3.x.x (JupyterLab 3 support) [#229](https://github.com/jupyterhub/jupyter-server-proxy/pull/229) ([@dipanjank](https://github.com/dipanjank))

#### Documentation improvements

- Bump to 1.6.0 (setup.py) and add CHANGELOG.md [#238](https://github.com/jupyterhub/jupyter-server-proxy/pull/238) ([@consideRatio](https://github.com/consideRatio))
- Replace server-process list with linkable headings [#236](https://github.com/jupyterhub/jupyter-server-proxy/pull/236) ([@manics](https://github.com/manics))
- Rename the mamba-navigator example to gator in the documentation [#234](https://github.com/jupyterhub/jupyter-server-proxy/pull/234) ([@jtpio](https://github.com/jtpio))

#### Contributors to this release

[@consideRatio](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3AconsideRatio+updated%3A2021-02-08..2021-02-25&type=Issues) | [@janjagusch](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Ajanjagusch+updated%3A2021-02-08..2021-02-25&type=Issues) | [@JanJaguschQC](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3AJanJaguschQC+updated%3A2021-02-08..2021-02-25&type=Issues) | [@jtpio](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Ajtpio+updated%3A2021-02-08..2021-02-25&type=Issues) | [@manics](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Amanics+updated%3A2021-02-08..2021-02-25&type=Issues) | [@ryanlovett](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Aryanlovett+updated%3A2021-02-08..2021-02-25&type=Issues) | [@yuvipanda](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-server-proxy+involves%3Ayuvipanda+updated%3A2021-02-08..2021-02-25&type=Issues)
