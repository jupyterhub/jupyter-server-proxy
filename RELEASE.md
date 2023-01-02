# How to make a release

`jupyter-server-proxy` is a package available on [PyPI][] and [conda-forge][].
These are instructions on how to make a release.

## Pre-requisites

- Push rights to [github.com/jupyterhub/jupyter-server-proxy][]
- Push rights to [conda-forge/jupyter-server-proxy-feedstock][]

## Steps to make a release

1. Create a PR updating `jupyterlab-server-proxy/yarn.lock` and continue only
   when its merged.

   This helps us avoid leaving known vulnerabilities are unfixed. To do this,
   delete the file and manually perform the the `build dist` step in the
   `.github/workflows/publish.yaml` workflow's `build` job as summarized below.

   ```shell
   rm jupyterlab-server-proxy/yarn.lock

   pip install jupyter_packaging wheel jupyterlab~=3.0
   python setup.py sdist bdist_wheel
   ```

2. Create a PR updating `docs/source/changelog.md` with [github-activity][] and
   continue only when its merged.

3. Checkout main and make sure it is up to date.

   ```shell
   git checkout main
   git fetch origin main
   git reset --hard origin/main
   ```

4. Update the version, make commits, and push a git tag with `tbump`.

   ```shell
   pip install tbump
   tbump --dry-run ${VERSION}

   # run
   tbump ${VERSION}
   ```

   Following this, the [CI system][] will build and publish a release.

5. Reset the version back to dev, e.g. `4.0.1.dev0` after releasing `4.0.0`.

   ```shell
   tbump --no-tag ${NEXT_VERSION}.dev0
   ```

6. Following the release to PyPI, an automated PR should arrive to
   [conda-forge/jupyter-server-proxy-feedstock][] with instructions.

[github-activity]: https://github.com/executablebooks/github-activity
[github.com/jupyterhub/jupyter-server-proxy]: https://github.com/jupyterhub/jupyter-server-proxy
[pypi]: https://pypi.org/project/jupyter-server-proxy/
[conda-forge]: https://anaconda.org/conda-forge/repo2docker_service
[conda-forge/jupyter-server-proxy-feedstock]: https://github.com/conda-forge/jupyter-server-proxy-feedstock
[ci system]: https://github.com/jupyterhub/jupyter-server-proxy/actions/workflows/release.yaml
