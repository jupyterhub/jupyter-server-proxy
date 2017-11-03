// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

import {
  JupyterLab, JupyterLabPlugin
} from '@jupyterlab/application';

import {
  ICommandPalette/*, IFrame, InstanceTracker*/
} from '@jupyterlab/apputils';

import {
    ServerConnection
} from '@jupyterlab/services';

import {
  ILauncher
} from '@jupyterlab/launcher';

import {
  Message
} from '@phosphor/messaging';

import '../style/index.css';

/**
 * The command IDs used by the rstudio plugin.
 */
namespace CommandIDs {
  export
  const launch = 'rsession:launch';
};

/**
 * The class name for the rstudio icon
 */
const RSTUDIO_ICON_CLASS = 'jp-RStudioIcon';


/**
 * Activate the rsession extension.
 */
function activate(app: JupyterLab, palette: ICommandPalette, launcher: ILauncher): void {
  let counter = 0;
  const category = 'RStudio';
  const namespace = 'rsession-proxy';
  const command = CommandIDs.launch;
  const { commands, shell } = app;

  commands.addCommand(command, {
    label: 'New Rstudio Session',
    caption: 'Start a new Rstudio Session',
    execute: () => {
      // Start up the rserver
      let settings = ServerConnection.makeSettings();
      let req = {
        url: settings.baseUrl + 'rsessionproxy',
        method: 'POST',
      };
      ServerConnection.makeRequest(req, settings).then((resp:ServerConnection.IResponse) => {
        console.log("Started RStudio... ", resp.data.url);
        window.open(resp.data.url, 'RStudio Session');
      });
    }
  });

  // Add a launcher item if the launcher is available.
  launcher.add({
    displayName: 'RStudio',
    iconClass: RSTUDIO_ICON_CLASS,
    callback: () => {
      return commands.execute(command);
    }
  });

  palette.addItem({ command, category });
}

/**
 * The rsession handler extension.
 */
const plugin: JupyterLabPlugin<void> = {
  id: 'jupyterlab_rsessionproxy',
  autoStart: true,
  requires: [ICommandPalette, ILauncher],
  activate: activate,
};


/**
 * Export the plugin as default.
 */
export default plugin;

