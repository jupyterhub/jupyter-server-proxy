import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { ILauncher } from '@jupyterlab/launcher';
import { PageConfig } from '@jupyterlab/coreutils';

import '../style/index.css';


function addLauncherEntries(serverData: any, launcher: ILauncher, app: JupyterFrontEnd) {
  for (let server_process of serverData.server_processes) {

    if (!server_process.launcher_entry.enabled) {
      continue;
    }

    let commandId = 'server-proxy:' + server_process.name;

    app.commands.addCommand(commandId, {
      label: server_process.launcher_entry.title,
      execute: () => {
        let launch_url = PageConfig.getBaseUrl() + server_process.name + '/';
        window.open(launch_url, '_blank');
      }
    });
    let command: ILauncher.IItemOptions = {
      command: commandId,
      category: 'Notebook'
    };
    if (server_process.launcher_entry.icon_url) {
      command.kernelIconUrl = server_process.launcher_entry.icon_url;
    }
    launcher.add(command);
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
