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
 * The identifying string names for server proxy commands.
 */
export namespace CommandIDs {
  /* Opens a new server proxy tab */
  export const open = `${NS}:open`;
}

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
 * An interface for the server response.
 */
export interface IServersInfo {
  server_processes: IServerProcess[];
}

/**
 * Public description of a single server process.
 */
export interface IServerProcess {
  new_browser_tab: boolean;
  launcher_entry: ILauncherEntry;
  name: string;
}

/**
 * Description of launcher information.
 */
export interface ILauncherEntry {
  enabled: boolean;
  title: string;
  path_info: string;
  icon_url?: string;
}

/**
 * The JSON schema for the open command arguments.
 *
 * https://lumino.readthedocs.io/en/latest/api/interfaces/commands.CommandRegistry.ICommandOptions.html
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
