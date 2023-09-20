import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
  ILayoutRestorer,
  ILabShell,
} from "@jupyterlab/application";
import { ReadonlyPartialJSONObject } from "@lumino/coreutils";
import { ILauncher } from "@jupyterlab/launcher";
import { PageConfig } from "@jupyterlab/coreutils";
import { IFrame, MainAreaWidget, WidgetTracker } from "@jupyterlab/apputils";

/** An interface for the arguments to the open command. */
export interface IOpenArgs extends ReadonlyPartialJSONObject {
  id: string;
  title: string;
  url: string;
  newBrowserTab: boolean;
}

/** The JSON schema for the open command arguments.
 *
 * https://lumino.readthedocs.io/en/latest/api/interfaces/commands.CommandRegistry.ICommandOptions.html
 */
export const argSchema = {
  type: "object",
  properties: {
    id: { type: "string" },
    title: { type: "string" },
    url: { type: "string", format: "uri" },
    newBrowserTab: { type: "boolean" },
  },
};

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

/**
 * The activate function is registered to be called on activation of the
 * jupyterlab extension.
 *
 * ref: https://jupyterlab.readthedocs.io/en/stable/extension/extension_dev.html
 */
async function activate(
  app: JupyterFrontEnd,
  labShell: ILabShell | null,
  launcher: ILauncher | null,
  restorer: ILayoutRestorer | null,
): Promise<void> {
  const baseUrl = PageConfig.getBaseUrl();
  // Fetch configured server processes from {base_url}/server-proxy/servers-info
  const response = await fetch(`${baseUrl}server-proxy/servers-info`);

  if (!response.ok) {
    console.warn(
      "Could not fetch metadata about registered servers. Make sure jupyter-server-proxy is installed.",
    );
    console.warn(response);
    return;
  }

  const data = await response.json();

  const namespace = "server-proxy";
  const tracker = new WidgetTracker<MainAreaWidget<IFrame>>({ namespace });
  const command = `${namespace}:open`;

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

  commands.addCommand(command, {
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

  if (launcher) {
    const baseUrl = PageConfig.getBaseUrl();
    for (let server_process of data.server_processes) {
      const { new_browser_tab, launcher_entry, name } = server_process;

      if (!launcher_entry.enabled) {
        continue;
      }

      launcher.add({
        command: command,
        args: {
          url: `${baseUrl}${launcher_entry.path_info}`,
          title: launcher_entry.title + (new_browser_tab ? " [↗]" : ""),
          newBrowserTab: new_browser_tab,
          id: `${namespace}:${name}`,
        },
        category: "Notebook",
        kernelIconUrl: launcher_entry.icon_url || void 0,
      });
    }
  }

  if (!labShell) {
    console.warn("TODO: handle notebook 7");
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
  optional: [ILabShell, ILauncher, ILayoutRestorer],
  activate: activate,
};

export default extension;
