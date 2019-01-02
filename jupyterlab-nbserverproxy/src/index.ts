import { JupyterLab, JupyterLabPlugin } from '@jupyterlab/application'; 
import { ILauncher } from '@jupyterlab/launcher';
import { PageConfig } from '@jupyterlab/coreutils';

import '../style/index.css';


function addLauncherEntries(serverData: any, launcher: ILauncher, app: JupyterLab) {
    for (let entry of serverData.launcher.entries) {

      let commandId = 'server-proxy:' + entry.name;
      app.commands.addCommand(commandId, {
        label: entry.title,
        execute: () => {
          let launch_url = PageConfig.getBaseUrl() + entry.name + '/';
          window.open(launch_url, '_blank');
        }
      });
      let iconUrl = PageConfig.getBaseUrl() + 'server-proxy/icon/' + entry.name;
      launcher.add({
        command: commandId,
        // This is the only way to get icon URLs in here
        category: 'Notebook',
        kernelIconUrl: iconUrl
      })
    }
}
/**
 * Initialization data for the jupyterlab-nbserverproxy extension.
 */
const extension: JupyterLabPlugin<void> = {
  id: 'jupyterlab-nbserverproxy',
  autoStart: true,
  requires: [ILauncher],
  activate: (app: JupyterLab, launcher: ILauncher) => {
    // FIXME: What the callback hell is this
    fetch(PageConfig.getBaseUrl() + 'server-proxy/servers-info').then(
      response => {
        if (!response.ok) {
          console.log('Fetching metadata about registered failed. Make sure nbserverproxy is installed');
          console.log(response);
        } else {
          response.json().then(data => addLauncherEntries(data, launcher, app))
        }

      }
    )
  }
};

export default extension;
