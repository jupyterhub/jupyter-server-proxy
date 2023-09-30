import { URLExt } from "@jupyterlab/coreutils";
import { showDialog, Dialog } from "@jupyterlab/apputils";
import { ServerConnection } from "@jupyterlab/services";
import { TranslationBundle } from "@jupyterlab/translation";
import { IModel } from "./serverproxy";

/**
 * The url for the server proxy service.
 */
const SERVER_PROXY_SERVICE_URL = "server-proxy/api/servers/";

/**
 * List the running server proxy apps.
 *
 * @param settings - The server settings to use.
 *
 * @returns A promise that resolves with the list of running session models.
 */
export async function listRunning(
  settings: ServerConnection.ISettings,
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
  trans: TranslationBundle,
  settings: ServerConnection.ISettings,
): Promise<void> {
  const url = URLExt.join(settings.baseUrl, SERVER_PROXY_SERVICE_URL, name);
  const init = { method: "DELETE" };
  const response = await ServerConnection.makeRequest(url, init, settings);
  if (response.status === 404) {
    const msg = trans.__(
      `Server proxy "${name}" is not running anymore. It will be removed from this list shortly`,
    );
    console.warn(msg);
    void showDialog({
      title: trans.__("Warning"),
      body: msg,
      buttons: [Dialog.okButton({ label: "Dismiss" })],
    });
  } else if (response.status === 403) {
    // This request cannot be made via JupyterLab UI and hence we just throw
    // console log
    const msg = trans.__(`Provide a running server proxy name to terminate`);
    console.warn(msg);
  } else if (response.status !== 204) {
    const err = await ServerConnection.ResponseError.create(response);
    throw err;
  }
}
