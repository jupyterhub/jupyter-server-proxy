// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

import {
  JupyterLab, JupyterLabPlugin
} from '@jupyterlab/application';

import {
  ICommandPalette, IMainMenu/*, IFrame, InstanceTracker*/
} from '@jupyterlab/apputils';

import {
  Message
} from '@phosphor/messaging';

import {
  Menu
} from '@phosphor/widgets';

import {
  PageConfig, URLExt
} from '@jupyterlab/coreutils';

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
function activate(app: JupyterLab, palette: ICommandPalette, mainMenu: IMainMenu): void {
  let counter = 0;
  const category = 'RStudio';
  const namespace = 'rsession-proxy';
  const command = CommandIDs.launch;
  const { commands, shell } = app;

  commands.addCommand(command, {
    label: 'Launch RStudio',
    caption: 'Start a new Rstudio Session',
    execute: () => {
        window.open(PageConfig.getBaseUrl() + 'rstudio/', 'RStudio Session');
    }
  });

  // Add commands and menu itmes.
  let menu = new Menu({ commands });
  menu.title.label = category;
  [
    CommandIDs.launch,
  ].forEach(command => {
    palette.addItem({ command, category });
    menu.addItem({ command });
  });
  mainMenu.addMenu(menu, {rank: 98});
}

/**
 * The rsession handler extension.
 */
const plugin: JupyterLabPlugin<void> = {
  id: 'jupyterlab_rsessionproxy',
  autoStart: true,
  requires: [ICommandPalette, IMainMenu],
  activate: activate,
};


/**
 * Export the plugin as default.
 */
export default plugin;

