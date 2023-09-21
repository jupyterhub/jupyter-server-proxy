import type { Widget, Menu } from "@lumino/widgets";

import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
  ILayoutRestorer,
} from "@jupyterlab/application";
import {
  IToolbarWidgetRegistry,
  IFrame,
  MainAreaWidget,
  WidgetTracker,
} from "@jupyterlab/apputils";
import { PageConfig, URLExt } from "@jupyterlab/coreutils";
import { IDefaultFileBrowser } from "@jupyterlab/filebrowser";
import { ILauncher } from "@jupyterlab/launcher";
import { ServerConnection } from "@jupyterlab/services";

import {
  CommandIDs,
  IOpenArgs,
  IServerProcess,
  IServersInfo,
  NS,
  argSchema,
} from "./tokens";

// top level constants that won't change during the application lifecycle
const baseUrl = PageConfig.getBaseUrl();
const notebookPage = PageConfig.getOption("notebookPage");
const isNotebook7 = !!notebookPage;
const isTree = isNotebook7 && notebookPage === "tree";

/** Create a new iframe widget. */
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

/** Generate command args for a given server. */
function argsForServer(server_process: IServerProcess): IOpenArgs {
  const { new_browser_tab, launcher_entry, name } = server_process;

  const suffix = new_browser_tab && !isNotebook7 ? " [↗]" : "";

  return {
    // do not use URLext here due to trailing slash opinions
    url: `${baseUrl}${launcher_entry.path_info}`,
    title: `${launcher_entry.title}${suffix}`,
    newBrowserTab: new_browser_tab,
    id: `${NS}:${name}`,
  };
}

/**
 * The activate function is registered to be called on activation of the
 * jupyterlab extension.
 *
 * ref: https://jupyterlab.readthedocs.io/en/stable/extension/extension_dev.html
 */
async function activate(
  app: JupyterFrontEnd,
  launcher: ILauncher | null,
  restorer: ILayoutRestorer | null,
  toolbarRegistry: IToolbarWidgetRegistry | null,
  fileBrowser: IDefaultFileBrowser | null,
): Promise<void> {
  // server connection settings _can't_ be a global, as it can be potentially be configured
  const serverSettings = ServerConnection.makeSettings();

  // Fetch configured server processes from {base_url}/server-proxy/servers-info
  // TODO: consider moving this to a separate plugin
  // TODO: consider not blocking the application load
  const url = URLExt.join(baseUrl, `${NS}/servers-info`);
  const response = await ServerConnection.makeRequest(url, {}, serverSettings);

  if (!response.ok) {
    console.warn(
      "Could not fetch metadata about registered servers. Make sure jupyter-server-proxy is installed.",
    );
    console.warn(response);
    return;
  }

  // TODO: consider adding JSON schema-derived types
  const data: IServersInfo = await response.json();

  // handle restoring persistent JupyterLab workspace widgets on page reload
  const tracker = new WidgetTracker<MainAreaWidget<IFrame>>({ namespace: NS });
  if (restorer) {
    void restorer.restore(tracker, {
      command: CommandIDs.open,
      args: (widget) => ({
        url: widget.content.url,
        title: widget.content.title.label,
        newBrowserTab: false,
        id: widget.content.id,
      }),
      name: (widget) => widget.content.id,
    });
  }

  // register commands
  const { commands, shell } = app;
  commands.addCommand(CommandIDs.open, {
    label: (args) => (args as IOpenArgs).title,
    describedBy: async () => {
      return { args: argSchema };
    },
    execute: (args) => {
      const { id, title, url, newBrowserTab } = args as IOpenArgs;
      if (newBrowserTab) {
        window.open(url, "_blank");
        return;
      }
      let widget = tracker.find((widget) => widget.content.id === id);
      if (!widget) {
        widget = newServerProxyWidget(id, url, title);
      }
      if (!tracker.has(widget)) {
        void tracker.add(widget);
      }
      if (!widget.isAttached) {
        shell.add(widget);
      } else {
        shell.activateById(widget.id);
      }
      return widget;
    },
  });

  // handle adding JupyterLab launcher cards
  // TODO: consider moving this to a separate plugin (keeping this ID)
  if (launcher) {
    for (let server_process of data.server_processes) {
      const { launcher_entry } = server_process;

      if (!launcher_entry.enabled) {
        continue;
      }

      launcher.add({
        command: CommandIDs.open,
        args: argsForServer(server_process),
        category: "Notebook",
        kernelIconUrl: launcher_entry.icon_url || void 0,
      });
    }
  }

  // handle adding servers menu items to the Notebook 7 _Tree_ toolbar
  // TODO: consider moving this to a separate plugin
  if (isTree && toolbarRegistry && fileBrowser) {
    const { toolbar } = fileBrowser;
    const widgets = ((toolbar.layout || {}) as any).widgets as Widget[];
    if (widgets && widgets.length) {
      for (const widget of widgets) {
        if (widget && (widget as any).menus) {
          // simple DOM queries can't be used, as there is no guarantee it is
          // attached yet
          const menu: Menu = (widget as any).menus[0];
          menu.addItem({ type: "separator" });
          for (const server_process of data.server_processes) {
            // create args, overriding all to launch in new heavyweight browser tabs
            let args = {
              ...argsForServer(server_process),
              newBrowserTab: true,
            };
            menu.addItem({ command: CommandIDs.open, args });
          }
        }
      }
    }
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
  optional: [
    ILauncher,
    ILayoutRestorer,
    IToolbarWidgetRegistry,
    IDefaultFileBrowser,
  ],
  activate,
};

export default extension;
