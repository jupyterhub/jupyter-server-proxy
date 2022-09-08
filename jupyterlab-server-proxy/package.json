{
  "name": "@jupyterlab/server-proxy",
  "version": "3.2.2",
  "description": "Jupyter server extension to supervise and proxy web services",
  "keywords": [
    "jupyter",
    "jupyterlab",
    "jupyterlab-extension"
  ],
  "homepage": "https://github.com/jupyterhub/jupyter-server-proxy",
  "bugs": {
    "url": "https://github.com/jupyterhub/jupyter-server-proxy/issues"
  },
  "license": "BSD-3-Clause",
  "author": {
    "name": "Ryan Lovett & Yuvi Panda",
    "email": "rylo@berkeley.edu"
  },
  "files": [
    "lib/**/*.{d.ts,eot,gif,html,jpg,js,js.map,json,png,svg,woff2,ttf}",
    "style/**/*.{css,eot,gif,html,jpg,json,png,svg,woff2,ttf}"
  ],
  "main": "lib/index.js",
  "types": "lib/index.d.ts",
  "repository": {
    "type": "git",
    "url": "https://github.com/jupyterhub/jupyter-server-proxy.git"
  },
  "scripts": {
    "build": "jlpm run build:lib && jlpm run build:labextension:dev",
    "build:prod": "jlpm run build:lib && jlpm run build:labextension",
    "build:labextension": "jupyter labextension build .",
    "build:labextension:dev": "jupyter labextension build --development True .",
    "build:lib": "tsc",
    "clean": "jlpm run clean:lib",
    "clean:lib": "rimraf lib tsconfig.tsbuildinfo",
    "clean:labextension": "rimraf jupyter_server_proxy/labextension",
    "clean:all": "jlpm run clean:lib && jlpm run clean:labextension",
    "eslint": "eslint . --ext .ts,.tsx --fix",
    "eslint:check": "eslint . --ext .ts,.tsx",
    "install:extension": "jupyter labextension develop --overwrite .",
    "watch": "run-p watch:src watch:labextension",
    "watch:src": "tsc -w",
    "watch:labextension": "jupyter labextension watch ."
  },
  "dependencies": {
    "@jupyterlab/application": "^2.0 || ^3.0",
    "@jupyterlab/launcher": "^2.0 || ^3.0"
  },
  "devDependencies": {
    "@jupyterlab/builder": "^3.2.4",
    "rimraf": "^2.6.1",
    "typescript": "~3.7.0"
  },
  "jupyterlab": {
    "extension": true,
    "outputDir": "../jupyter_server_proxy/labextension"
  }
}
