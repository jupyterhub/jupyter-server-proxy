// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

import {
  ILayoutRestorer, JupyterLab, JupyterLabPlugin
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
 * A flag denoting whether the application is loaded over HTTPS.
 */
// const LAB_IS_SECURE = window.location.protocol === 'https:';

/**
 * The class name added to the help widget.
 */
// const RSESSION_CLASS = 'jp-Rsession';

/**
 * A list of help resources.
 */

const RESOURCES = [
  {
    text: 'RStudio Session',
    url: '/'
  }
];

RESOURCES.sort((a: any, b: any) => {
  return a.text.localeCompare(b.text);
});


/**
 * The rsession handler extension.
 */
const plugin: JupyterLabPlugin<void> = {
  activate,
  id: 'jupyter.extensions.rsessionproxy',
  requires: [ICommandPalette, ILayoutRestorer],
  optional: [ILauncher],
  autoStart: true
};


/**
 * Export the plugin as default.
 */
export default plugin;

/*
  * An IFrame the disposes itself when closed.
  *
  * This is needed to clear the state restoration db when IFrames are closed.
 */
// class ClosableIFrame extends IFrame {
//
//   /**
//    * Dispose of the IFrame when closing.
//    */
//   protected onCloseRequest(msg: Message): void {
//     this.dispose();
//   }
// }


/**
 * Activate the rsession extension.
 */
function activate(app: JupyterLab, palette: ICommandPalette,
                  restorer: ILayoutRestorer, launcher: ILauncher | null): void {
  let counter = 0;
  const category = 'RStudio';
  const namespace = 'rsession-proxy';
  const command = CommandIDs.launch;
  const { commands, shell } = app;
  // const tracker = new InstanceTracker<ClosableIFrame>({ namespace });

  // Handle state restoration.
  // restorer.restore(tracker, {
  //   command,
  //   args: widget => ({ url: widget.url, text: widget.title.label }),
  //   name: widget => widget.url
  // });

  /**
   * Create a new ClosableIFrame widget.
   */
  // function newClosableIFrame(url: string, text: string): ClosableIFrame {
  //   let iframe = new ClosableIFrame();
  //   iframe.addClass(RSESSION_CLASS);
  //   iframe.title.label = text;
  //   iframe.title.closable = true;
  //   iframe.id = `${namespace}-${++counter}`;
  //   iframe.url = url;
  //   tracker.add(iframe);
  //   return iframe;
  // }

  commands.addCommand(command, {
    label: 'New Rstudio Session',
    caption: 'Start a new Rstudio Session',
    execute: () => {
      // Start up the rserver
      let settings = ServerConnection.makeSettings();
      let req = {
        url: settings.baseUrl + 'rsessionproxy',
        method: 'POST',
        data: {}
      };
      ServerConnection.makeRequest(req, settings).then(resp => {
        console.log("Started RStudio... ", resp.data.url);
        window.open(resp.data.url, 'RStudio Session');
        // let iframe = newClosableIFrame(resp.data.url, 'Rstudio Session');
        // shell.addToMainArea(iframe);
        // shell.activateById(iframe.id);
      });
    }
  });

  // Add a launcher item if the launcher is available.
  if (launcher) {
    launcher.add({
      displayName: 'RStudio',
      iconClass: RSTUDIO_ICON_CLASS,
      callback: () => {
        return commands.execute(command);
      }
    });
  }

  palette.addItem({ command, category });
}

