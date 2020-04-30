import { JupyterFrontEnd, JupyterFrontEndPlugin, ILayoutRestorer } from '@jupyterlab/application';
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

async function activate(app: JupyterFrontEnd, launcher: ILauncher, restorer: ILayoutRestorer) : Promise<void> {
  const response = await fetch(PageConfig.getBaseUrl() + 'server-proxy/servers-info');
  if (!response.ok) {
    console.log('Fetching metadata about registered failed. Make sure jupyter-server-proxy is installed');
    console.log(response);
    return;
  }

  const data = await response.json();
  for (let server_process of data.server_processes) {
    const namespace = 'server-proxy' + ':' + server_process.name;
    const command = namespace + ':' + 'open';

    const launch_url = PageConfig.getBaseUrl() + server_process.name + '/';
    let widget : MainAreaWidget<IFrame>;
    const options : CommandRegistry.ICommandOptions = {
      label: server_process.launcher_entry.title,
      execute: (server_process.framed?
        () => {
          if (!widget || widget.isDisposed) {
            widget = newServerProxyWidget(command, launch_url, server_process.launcher_entry.title);
          }
          if (!widget.isAttached) {
            app.shell.add(widget);
          }
          if (!tracker.has(widget)) {
            void tracker.add(widget);
          }
          app.shell.activateById(widget.id);
        }
        :
        () => window.open(launch_url, '_blank')
      )
    };

    app.commands.addCommand(command, options);

    let tracker = new WidgetTracker<MainAreaWidget<IFrame>>({
      namespace: server_process.name
    });

    restorer.restore(tracker, {
      command,
      name: () => server_process.name
    });

    if (!server_process.launcher_entry.enabled) {
      continue;
    }

    const launcher_item : ILauncher.IItemOptions = {
      command: command,
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
  requires: [ILauncher, ILayoutRestorer],
  activate: activate
};

export default extension;
