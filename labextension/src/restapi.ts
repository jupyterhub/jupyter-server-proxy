import { URLExt } from "@jupyterlab/coreutils";
import { ServerConnection } from "@jupyterlab/services";
import { IModel } from "./serverproxy";

/**
 * The url for the server proxy service.
 */
const SERVER_PROXY_SERVICE_URL = "api/server-proxy";

/**
 * List the running server proxy apps.
 *
 * @param settings - The server settings to use.
 *
 * @returns A promise that resolves with the list of running session models.
 */
export async function listRunning(
  settings: ServerConnection.ISettings = ServerConnection.makeSettings(),
): Promise<IModel[]> {
  const url = URLExt.join(settings.baseUrl, SERVER_PROXY_SERVICE_URL);
  const response = await ServerConnection.makeRequest(url, {}, settings);
  if (response.status !== 200) {
    const err = await ServerConnection.ResponseError.create(response);
    throw err;
  }
  const data = await response.json();

  if (!Array.isArray(data)) {
    throw new Error("Invalid server proxy list");
  }

  return data;
}

/**
 * Shut down a server proxy app by name.
 *
 * @param name - The name of the target server proxy app.
 *
 * @param settings - The server settings to use.
 *
 * @returns A promise that resolves when the app is shut down.
 */
export async function shutdown(
  name: string,
  settings: ServerConnection.ISettings = ServerConnection.makeSettings(),
): Promise<void> {
  const url = URLExt.join(settings.baseUrl, SERVER_PROXY_SERVICE_URL, name);
  const init = { method: "DELETE" };
  const response = await ServerConnection.makeRequest(url, init, settings);
  if (response.status === 404) {
    const msg = `Server proxy "${name}" does not exist. Are you sure "${name}" is started by jupyter-server-proxy?`;
    console.warn(msg);
  } else if (response.status !== 204) {
    const err = await ServerConnection.ResponseError.create(response);
    throw err;
  }
}
