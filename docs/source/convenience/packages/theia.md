# Theia IDE

[Theia](https://theia-ide.org/) is a configurable web based IDE
built with components from [Visual Studio Code](https://code.visualstudio.com/).

This package is a plugin for [jupyter-server-proxy](https://jupyter-server-proxy.readthedocs.io/)
that lets you run an instance of theia alongside your notebook, primarily
in a JupyterHub / Binder environment.

## Installing Theia

1. [Install the Yarn package manager](https://classic.yarnpkg.com/en/docs/install/) with one of the available
   methods.

2. Theia is highly configurable, so you need to decide which features you want
   in your theia install. Make a `package.json` with the list of extensions you want,
   following [the instructions here](https://theia-ide.org/docs/composing_applications/).

   Here is an example:

   ```js
   {
     "private": true,
     "dependencies": {
         "@theia/callhierarchy": "latest",
         "@theia/editor-preview": "latest",
         "@theia/file-search": "latest",
         "@theia/git": "latest",
         "@theia/json": "latest",
         "@theia/languages": "latest",
         "@theia/markers": "latest",
         "@theia/merge-conflicts": "latest",
         "@theia/messages": "latest",
         "@theia/mini-browser": "latest",
         "@theia/monaco": "latest",
         "@theia/navigator": "latest",
         "@theia/outline-view": "latest",
         "@theia/preferences": "latest",
         "@theia/preview": "latest",
         "@theia/python": "latest",
         "@theia/search-in-workspace": "latest",
         "@theia/terminal": "latest",
         "@theia/textmate-grammars": "latest",
         "@theia/typescript": "latest",
         "typescript": "latest",
         "yarn": "^1.12.3"
     },
     "devDependencies": {
         "@theia/cli": "latest"
     }
   }
   ```

3. Run the following commands in the same location as your package.json file
   to install all packages & build theia.

   ```bash
   yarn
   yarn theia build
   ```

   This should set up theia to run and be built.

4. Add the `node_modules/.bin` directory to your `$PATH`, so `jupyter-theia-proxy` can
   find the `theia` command.

   ```bash
   export PATH="$(pwd)/node_modules/.bin:${PATH}"
   ```
