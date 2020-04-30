import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application'; 
import { ILauncher } from '@jupyterlab/launcher';
import { PageConfig } from '@jupyterlab/coreutils';
import { IFrame } from '@jupyterlab/apputils';

import { CommandRegistry } from '@lumino/commands';

import '../style/index.css';

function addLauncherEntries(serverData: any, launcher: ILauncher, app: JupyterFrontEnd) {
    for (let server_process of serverData.server_processes) {
      let commandId = 'server-proxy:' + server_process.name;
      let launch_url = PageConfig.getBaseUrl() + server_process.name + '/';
      let options : CommandRegistry.ICommandOptions;

      if (server_process.framed) {
        let iframe = new IFrame();
        iframe.sandbox = ['allow-same-origin', 'allow-scripts', 'allow-popups', 'allow-forms'];
        iframe.title.label = server_process.launcher_entry.title;
        iframe.title.closable = true;
        iframe.url = launch_url;
        iframe.id = commandId;
        options = {
          label: server_process.launcher_entry.title,
          execute: () => {
            if (!iframe.isAttached) {
              app.shell.add(iframe);
            }
            app.shell.activateById(iframe.id);
          }
        }
      } else {
        options = {
          label: server_process.launcher_entry.title,
          execute: () => {
            window.open(launch_url, '_blank');
          }
        }
      }
      
      app.commands.addCommand(commandId, options);
      if (!server_process.launcher_entry.enabled) {
        continue;
      }

      let launcher_item : ILauncher.IItemOptions = {
        command: commandId,
        category: 'Notebook'
      };
      if (server_process.launcher_entry.icon_url) {
        launcher_item.kernelIconUrl =  server_process.launcher_entry.icon_url;
      }
      launcher.add(launcher_item);
    }
}
/**
 * Initialization data for the jupyterlab-server-proxy extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab-server-proxy',
  autoStart: true,
  requires: [ILauncher],
  activate: (app: JupyterFrontEnd, launcher: ILauncher) => {
    // FIXME: What the callback hell is this
    fetch(PageConfig.getBaseUrl() + 'server-proxy/servers-info').then(
      response => {
        if (!response.ok) {
          console.log('Fetching metadata about registered failed. Make sure jupyter-server-proxy is installed');
          console.log(response);
        } else {
          response.json().then(data => addLauncherEntries(data, launcher, app))
        }

      }
    )
  }
};

export default extension;
