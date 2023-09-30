import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
  ILayoutRestorer,
} from "@jupyterlab/application";
import { ILauncher } from "@jupyterlab/launcher";
import { PageConfig, URLExt } from "@jupyterlab/coreutils";
import { IRunningSessionManagers } from "@jupyterlab/running";
import { ISettingRegistry } from "@jupyterlab/settingregistry";
import { ITranslator, TranslationBundle } from "@jupyterlab/translation";
import { IFrame, MainAreaWidget, WidgetTracker } from "@jupyterlab/apputils";
import { ServerProxyManager } from "./manager";
import { IModel as IServerProxyModel } from "./serverproxy";
import { RunningServerProxyApp, CommandIDs } from "./running";

function newServerProxyWidget(
  id: string,
  url: string,
  text: string,
): MainAreaWidget<IFrame> {
  const content = new IFrame({
    sandbox: [
      "allow-same-origin",
      "allow-scripts",
      "allow-popups",
      "allow-forms",
      "allow-downloads",
      "allow-modals",
    ],
  });
  content.title.label = text;
  content.title.closable = true;
  content.url = url;
  content.addClass("jp-ServerProxy");
  content.id = id;
  const widget = new MainAreaWidget({ content });
  widget.addClass("jp-ServerProxy");
  return widget;
}

/**
 * This function adds the active server proxy applications to running sessions
 * so that user can track currently running applications via server proxy.
 * User can shut down the applications as well to restart them in future
 *
 */
function addRunningSessionManager(
  managers: IRunningSessionManagers,
  app: JupyterFrontEnd,
  manager: ServerProxyManager,
  trans: TranslationBundle,
): void {
  managers.add({
    name: "Server Proxy Apps",
    running: () =>
      Array.from(manager.running()).map(
        (model) => new RunningServerProxyApp(model, manager, app),
      ),
    shutdownAll: () => manager.shutdownAll(),
    refreshRunning: () => manager.refreshRunning(),
    runningChanged: manager.runningChanged,
    shutdownAllConfirmationText: trans.__(
      "Are you sure you want to close all server proxy applications?",
    ),
  });
}

/**
 * The activate function is registered to be called on activation of the
 * jupyterlab extension.
 *
 * ref: https://jupyterlab.readthedocs.io/en/stable/extension/extension_dev.html
 */
async function activate(
  app: JupyterFrontEnd,
  launcher: ILauncher,
  restorer: ILayoutRestorer,
  settingRegistry: ISettingRegistry,
  translator: ITranslator,
  sessions: IRunningSessionManagers | null,
): Promise<void> {
  const trans = translator.load("jupyter-server-proxy");

  // Fetch configured server processes from {base_url}/server-proxy/servers-info
  const response = await fetch(
    URLExt.join(PageConfig.getBaseUrl(), "server-proxy/api/servers-info"),
  );
  if (!response.ok) {
    console.log(
      trans.__(
        "Could not fetch metadata about registered servers. Make sure jupyter-server-proxy is installed.",
      ),
    );
    console.log(response);
    return;
  }
  const data = await response.json();

  // Load application settings
  const settings = await settingRegistry.load(extension.id);

  const namespace = "server-proxy";
  const tracker = new WidgetTracker<MainAreaWidget<IFrame>>({
    namespace,
  });
  const command = namespace + ":" + "open";

  if (restorer) {
    void restorer.restore(tracker, {
      command: command,
      args: (widget) => ({
        url: widget.content.url,
        title: widget.content.title.label,
        newBrowserTab: false,
        id: widget.content.id,
      }),
      name: (widget) => widget.content.id,
    });
  }

  const { commands, shell } = app;

  // Add server proxy session manager to running sessions
  if (sessions) {
    let manager = new ServerProxyManager({ trans, settings });
    addRunningSessionManager(sessions, app, manager, trans);
  }

  commands.addCommand(command, {
    label: (args) => args["title"] as string,
    execute: (args) => {
      const id = args["id"] as string;
      const title = args["title"] as string;
      const url = args["url"] as string;
      const newBrowserTab = args["newBrowserTab"] as boolean;
      if (newBrowserTab) {
        window.open(url, "_blank");
        return;
      }
      let widget = tracker.find((widget) => {
        return widget.content.id == id;
      });
      if (!widget) {
        widget = newServerProxyWidget(id, url, title);
      }
      if (!tracker.has(widget)) {
        void tracker.add(widget);
      }
      if (!widget.isAttached) {
        shell.add(widget);
        return widget;
      } else {
        shell.activateById(widget.id);
      }
    },
  });

  commands.addCommand(CommandIDs.open, {
    execute: (args) => {
      const model = args["sp"] as IServerProxyModel;
      const url = URLExt.join(PageConfig.getBaseUrl(), model.url);
      window.open(url, "_blank");
      return;
    },
  });

  for (let server_process of data.server_processes) {
    if (!server_process.launcher_entry.enabled) {
      continue;
    }

    const url = URLExt.join(
      PageConfig.getBaseUrl(),
      server_process.launcher_entry.path_info,
    );
    const title = server_process.launcher_entry.title;
    const newBrowserTab = server_process.new_browser_tab;
    const id = namespace + ":" + server_process.name;
    const launcher_item: ILauncher.IItemOptions = {
      command: command,
      args: {
        url: url,
        title: title + (newBrowserTab ? " [↗]" : ""),
        newBrowserTab: newBrowserTab,
        id: id,
      },
      category: "Notebook",
    };

    if (server_process.launcher_entry.icon_url) {
      launcher_item.kernelIconUrl = server_process.launcher_entry.icon_url;
    }
    launcher.add(launcher_item);
  }
}

/**
 * Data to register the extension with jupyterlab which also clarifies whats
 * required by the extension and passed to our provided activate function.
 *
 * ref: https://jupyterlab.readthedocs.io/en/stable/extension/extension_dev.html#application-plugins
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: "@jupyterhub/jupyter-server-proxy:add-launcher-entries",
  autoStart: true,
  requires: [ILauncher, ILayoutRestorer, ISettingRegistry, ITranslator],
  optional: [IRunningSessionManagers],
  activate: activate,
};

export default extension;
