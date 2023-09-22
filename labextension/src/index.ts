/**
 * The main extension file, which provides plugins that can be loaded into
 * a Lumino application such as JupyterLab or Notebook 7.
 *
 * Outside of this file, of note is `./tokens.ts`, which provides a number of
 * run-time constants and compile-type interfaces for type-checking.
 *
 * Imports (mostly) adhere to the ES `import` semantics, exceptions noted below
 * @see https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import
 */

// this is a type-only import for low-level components of the UI
// @see https://www.typescriptlang.org/docs/handbook/release-notes/typescript-3-8.html
import type {
  // the base class for all on-screen components
  Widget,
  // the Lumino component for menu bars
  Menu,
} from "@lumino/widgets";

import {
  // the dependency-injection (DI) Token required to request a dependency for...
  ILayoutRestorer,
  // any lumino-based Jupyter application...
  JupyterFrontEnd,
  // to be extended with...
  JupyterFrontEndPlugin,
} from "@jupyterlab/application";
import {
  // a DI token for the toolbar, used to extend Notebook's Tree
  IToolbarWidgetRegistry,
  // the concrete class used to create iframes in the JupyterLab main area
  IFrame,
  // a wrapper for the iframe that handles house-keeping boilerplate
  MainAreaWidget,
  // a tracker which handles iframe placement housekeeping when JupyterLab is reloaded
  WidgetTracker,
} from "@jupyterlab/apputils";
// utilities for working with URLs and the `jupyter-config-data` script
import { PageConfig, URLExt } from "@jupyterlab/coreutils";
// a DI token for the file browser, present in JupyterLab and Notebook 7
import { IDefaultFileBrowser } from "@jupyterlab/filebrowser";
// a DI token for the card-based Launcher, present in JupyterLab
import { ILauncher } from "@jupyterlab/launcher";
// the application-wide configuration for making HTTP requests with headers, etc.
import { ServerConnection } from "@jupyterlab/services";

// local imports from `tokens.ts` for immutable constants
import {
  CommandIDs,
  IOpenArgs,
  IServerProcess,
  IServersInfo,
  NAME,
  NS,
  argSchema,
  sandbox,
} from "./tokens";

/*
 * top level constants that won't change during the application lifecycle
 */
const baseUrl = PageConfig.getBaseUrl();
/**
 * The Notebook 7 sub-application: `tree`, `notebook`, `editor`, `terminal`, etc.
 */
const notebookPage = PageConfig.getOption("notebookPage");
/**
 * Whether the current application is `/tree`: otherwise we don't do anything
 */
const isTree = notebookPage === "tree";
/**
 * Whether this is a notebook app at all
 */
const isNotebook7 = !!notebookPage;

/**
 * Data to register the extension with jupyterlab which also clarifies the shape of
 * what is required by the extension and passed to our provided activate function.
 *
 * This plugin is `export`ed at the end of the file.
 *
 * @see https://jupyterlab.readthedocs.io/en/stable/extension/extension_dev.html#application-plugins
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: `${NAME}:add-launcher-entries`,
  autoStart: true,
  // to support JupyterLab and Notebook, we don't _require_ any other DI tokens...
  requires: [],
  // ... but some decisions will be made on the presence of these optional DI tokens,
  //     which will be given to `activate` in the order listed here
  optional: [
    ILauncher,
    ILayoutRestorer,
    IToolbarWidgetRegistry,
    IDefaultFileBrowser,
  ],
  activate,
};

/**
 * The activate function is registered to be called on activation of the
 * JupyterLab/Notebook 7 plugin.
 *
 * @see https://jupyterlab.readthedocs.io/en/stable/extension/extension_dev.html
 */
async function activate(
  app: JupyterFrontEnd,
  // `requires` would have show up here with concrete types ...
  // ... but all `optional` DI tokens _might_ be `null`
  launcher: ILauncher | null,
  restorer: ILayoutRestorer | null,
  toolbarRegistry: IToolbarWidgetRegistry | null,
  fileBrowser: IDefaultFileBrowser | null,
): Promise<void> {
  // when viewing `/notebook`, `/terminal` or `/editor`, bail as early as possible
  if (isNotebook7 && !isTree) {
    return;
  }

  // server connection settings (such as headers) _can't_ be a global, as they
  // can potentially be configured by other extensions
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

  // load and trust the JSON as a type of data described by the `IServersInfo` interface
  // TODO: consider adding JSON schema-derived types
  const data = (await response.json()) as IServersInfo;

  // handle restoring persistent JupyterLab workspace widgets on page reload
  // this is created even in the Notebook `tree` page to reduce complexity below
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
  // commands provide "loose" coupling, based on well-known strings and JSON-like
  // structures instead of heavy DI tokens
  const { commands, shell } = app;
  commands.addCommand(CommandIDs.open, {
    label: (args) => (args as IOpenArgs).title,
    describedBy: async () => {
      return { args: argSchema };
    },
    execute: (args) => {
      // the syntax below is an example of "destructuring"
      // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment
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
 * Create a new `iframe`, with a wrapper for including in the main area.
 */
function newServerProxyWidget(
  id: string,
  url: string,
  text: string,
): MainAreaWidget<IFrame> {
  const content = new IFrame({
    // provide relatively permissing sandbox exceptions
    sandbox,
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
 * Generate command arguments for a given server.
 *
 * @see https://lumino.readthedocs.io/en/latest/api/interfaces/commands.CommandRegistry.ICommandOptions.html
 *
 * For parity with Notebook Classic, any server opened from the Tree will be loaded
 * in a new browser tab.
 */
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

// finally, export the plugin...
export default plugin;
// in the future, the above could be an array of plugins, to provide finer-grained
// or replaceable implementations
