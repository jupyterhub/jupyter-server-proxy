import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { ILauncher } from '@jupyterlab/launcher';
import { PageConfig } from '@jupyterlab/coreutils';
import { IFrame, MainAreaWidget, WidgetTracker } from '@jupyterlab/apputils';

import { CommandRegistry } from '@lumino/commands';

import '../style/index.css';

function newServerProxyWidget(id: string, url: string, text: string): MainAreaWidget<IFrame> {
  const content = new IFrame({
    sandbox: ['allow-same-origin', 'allow-scripts', 'allow-popups', 'allow-forms'],
  });
  content.title.label = text;
  content.title.closable = true;
  content.url = url;
  content.addClass('jp-ServerProxy');
  content.id = id;
  const widget = new MainAreaWidget({ content });
  widget.addClass('jp-ServerProxy');
  return widget;
}

function addLauncherEntries(serverData: any, launcher: ILauncher, app: JupyterFrontEnd) {

    const namespace = 'server-proxy';
    const tracker = new WidgetTracker<MainAreaWidget<IFrame>>({ namespace });

    for (let server_process of serverData.server_processes) {
      const commandId = namespace + ':' + server_process.name;
      const launch_url = PageConfig.getBaseUrl() + server_process.name + '/';
      const widget = newServerProxyWidget(commandId, launch_url, server_process.launcher_entry.title);
      const options : CommandRegistry.ICommandOptions = {
        label: server_process.launcher_entry.title,
        execute: (server_process.framed?
          () => {
            if (!widget.isAttached) {
              app.shell.add(widget);
              void tracker.add(widget);
            }
            app.shell.activateById(widget.id);
          }
          :
          () => window.open(launch_url, '_blank')
        )
      };

      app.commands.addCommand(commandId, options);
      
      if (!server_process.launcher_entry.enabled) {
        continue;
      }
      const launcher_item : ILauncher.IItemOptions = {
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
