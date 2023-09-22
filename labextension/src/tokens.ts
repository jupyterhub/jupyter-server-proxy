/**
 * A collection of tokens and constants used in `index.ts`.
 *
 * `import`ing this file should have basically no side-effects.
 */

import type { IFrame } from "@jupyterlab/apputils";

import type { ReadonlyJSONObject } from "@lumino/coreutils";

/**
 * The canonical name of the extension, also used in CLI commands such as
 * `jupyter labextension disable`.
 */
export const NAME = "@jupyterhub/jupyter-server-proxy";

/**
 * The short namespace for commands, etc.
 */
export const NS = "server-proxy";

/**
 * The values for the `iframe` `sandbox` attribute.
 *
 * These are generally required for most non-trivial client applications, but
 * do not affect full browser tabs.
 *
 * @see https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/sandbox
 */
export const sandbox = Object.freeze([
  "allow-same-origin",
  "allow-scripts",
  "allow-popups",
  "allow-forms",
  "allow-downloads",
  "allow-modals",
]) as IFrame.SandboxExceptions[];

/**
 * The JSON schema for the open command arguments.
 *
 * @see https://lumino.readthedocs.io/en/latest/api/interfaces/commands.CommandRegistry.ICommandOptions.html
 */
export const argSchema = Object.freeze({
  type: "object",
  properties: {
    id: { type: "string" },
    title: { type: "string" },
    url: { type: "string", format: "uri" },
    newBrowserTab: { type: "boolean" },
  },
});

/**
 * The identifying string names for server proxy commands.
 *
 * Namespaces are real objects that exist at runtime in the browser
 *
 * @see https://www.typescriptlang.org/docs/handbook/namespaces.html
 */
export namespace CommandIDs {
  /* Opens a new server proxy tab */
  export const open = `${NS}:open`;
}

// Below here are TypeScript interfaces. These do _not_ exist at runtime
// but are useful when working with untyped data such as provided by the server
// @see https://www.typescriptlang.org/docs/handbook/interfaces.html

/**
 * An interface for the arguments to the open command.
 */
export interface IOpenArgs extends ReadonlyJSONObject {
  id: string;
  title: string;
  url: string;
  newBrowserTab: boolean;
}

/**
 * An interface for the server response from `/server-proxy/servers-info`
 */
export interface IServersInfo {
  server_processes: IServerProcess[];
}

/**
 * An interface for the public description of a single server proxy.
 */
export interface IServerProcess {
  new_browser_tab: boolean;
  launcher_entry: ILauncherEntry;
  name: string;
}

/**
 * An interface for launcher-card specific information.
 */
export interface ILauncherEntry {
  enabled: boolean;
  title: string;
  path_info: string;
  // the `?` means this argument may not exist, but if it does, it must be a string
  icon_url?: string;
}
