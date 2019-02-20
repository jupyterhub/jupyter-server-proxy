import { JupyterLab, JupyterLabPlugin } from '@jupyterlab/application';
import { CommandRegistry } from '@phosphor/commands';
import { ILauncher } from '@jupyterlab/launcher';
import { PageConfig } from '@jupyterlab/coreutils';

import '../style/index.css';

/**
 * JSON response expected from /server-proxy/servers-info/
 */
export interface ServersInfo {
  server_processes: Server[];
}

/**
 * JSON Proxy Server entry
 */
export interface Server {
  name: string;
  launcher_entry: {
    enabled: boolean;
    title: string;
    icon_url?: string;
  }
}

/**
 * Initialization data for the jupyterlab-server-proxy extension.
 */
const extension: JupyterLabPlugin<void> = {
  id: 'jupyterlab-server-proxy',
  autoStart: true,
  requires: [ILauncher],
  activate: async (app: JupyterLab, launcher: ILauncher) => {
    const response = await fetch(PageConfig.getBaseUrl() + 'server-proxy/servers-info/');
    if (!response.ok) {
      console.warn('Fetching metadata about registered services failed.')
      console.info('Make sure jupyter-server-proxy is installed');
      console.debug(response);
    } else {
      addLauncherEntries(await response.json(), launcher, app.commands);
    }
  }
};

export default extension;

/**
 * Add JupyterLab commands and Launcher cards for server proxies
 */
function addLauncherEntries(
  serverData: ServersInfo,
  launcher: ILauncher,
  commands: CommandRegistry
) {
  const style = document.createElement('style');
  document.head.appendChild(style);

  for (const { name, launcher_entry } of serverData.server_processes) {
    const { icon_url, enabled, title } = launcher_entry;

    if (!enabled) {
      continue;
    }

    const command = `server-proxy:${name}`;

    const commandOptions: CommandRegistry.ICommandOptions = {
      label: title,
      execute: () => {
        window.open(PageConfig.getBaseUrl() + name + '/', '_blank');
      },
    };

    if (icon_url) {
      commandOptions.iconClass = `jp-ServerProxy-icon-${name}`;
      style.textContent += `.${commandOptions.iconClass} {background-image: url(${icon_url});}`;
    }

    commands.addCommand(command, commandOptions);
    launcher.add({ command, category: 'Notebook' });
  }
}
