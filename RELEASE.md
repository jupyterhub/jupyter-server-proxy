# How to make a release

`jupyter-server-proxy` is a package [available on
PyPI](https://pypi.org/project/jupyter-server-proxy/) and
[conda-forge](https://github.com/conda-forge/jupyter-server-proxy-feedstock).
These are instructions on how to make a release on PyPI. The PyPI release is
done automatically by [GitHub
Actions](https://github.com/jupyterhub/jupyter-server-proxy/actions/workflows/publish.yaml)
when a tag is pushed.

For you to follow along according to these instructions, you need:

- To have push rights to the [jupyter-server-proxy GitHub
  repository](https://github.com/jupyterhub/jupyter-server-proxy).

## Steps to make before a release

1. Consider updating jupyterlab-server-proxy/yarl.lock to avoid a build
   environment with potential known vulnerabilities. At least check in at
   https://github.com/jupyterhub/jupyter-server-proxy/security/dependabot to
   make sure no known vulnerabilities are listed.

   If you want to update jupyterlab-server-proxy/yarl.lock, you can do so by
   deleting the file and doing the first step of the GitHub workflow we have
   defined to publish the PyPI package and the NPM package.

   ```shell
   pip install -U jupyter_packaging wheel "jupyterlab==3.*"
   python setup.py sdist bdist_wheel
   ```

2. Update [CHANGELOG.md](CHANGELOG.md). Doing this can be made easier with the
   help of the
   [choldgraf/github-activity](https://github.com/choldgraf/github-activity)
   utility.

## Steps to make a release

1. Checkout `main` and make sure it is up to date.

   ```shell
   ORIGIN=${ORIGIN:-origin} # set to the canonical remote, e.g. 'upstream' if 'origin' is not the official repo
   git checkout main
   git fetch $ORIGIN main
   git reset --hard $ORIGIN/main
   # WARNING! This next command deletes any untracked files in the repo
   git clean -xfd
   ```

1. Set the `version` variable in
   [jupyterlab-server-proxy/package.json](jupyterlab-server-proxy/package.json)
   appropriately and make a commit. Note that setup.py will read this from
   jupyterlab-server-proxy/package.json.

   ```
   git add jupyterlab-server-proxy/package.json
   VERSION=...  # e.g. 1.2.3
   git commit -m "release v$VERSION"
   ```

2. Push your commit to main.

   ```shell
   # first push commits without a tags to ensure the
   # commits comes through, because a tag can otherwise
   # be pushed all alone without company of rejected
   # commits, and we want have our tagged release coupled
   # with a specific commit in main
   git push $ORIGIN main
   ```

3. Create a git tag for the pushed release commit and push it.

   ```shell
   git tag -a v$VERSION -m v$VERSION HEAD

   # then verify you tagged the right commit
   git log

   # then push it
   git push $ORIGIN refs/tags/v$VERSION
   ```

4. Following the release to PyPI, an automated PR should arrive to
   [conda-forge/jupyter-server-proxy-feedstock](https://github.com/conda-forge/oauthenticator-feedstock),
   check for the tests to succeed on this PR and then merge it to successfully
   update the package for `conda` on the conda-forge channel.
