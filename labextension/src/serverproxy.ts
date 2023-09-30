import { JSONObject } from "@lumino/coreutils";
import { ISignal } from "@lumino/signaling";
import { IManager as IBaseManager } from "@jupyterlab/services";

/**
 * The server model for a proxy.
 */
export interface IModel extends JSONObject {
  /**
   * The name of the proxy app.
   */
  readonly name: string;

  /**
   * The cmd used to launch proxy app.
   */
  readonly cmd: string;

  /**
   * The port at which proxy app is running. Port 0 means unix socket.
   */
  readonly port: string;

  /**
   * The url endpoint of the proxy app.
   */
  readonly url: string;

  /**
   * Proxy app managed by jupyter-server-proxy or not.
   */
  readonly managed: boolean;

  /**
   * Proxy app managed by jupyter-server-proxy or not.
   */
  readonly unix_socket: string;
}

/**
 * The interface for a server proxy manager.
 *
 * The manager is responsible for maintaining the state of running
 * server proxy apps.
 */
export interface IManager extends IBaseManager {
  /**
   * A signal emitted when the running server proxy apps change.
   */
  runningChanged: ISignal<IManager, IModel[]>;

  /**
   * Create an iterator over the known server proxy apps.
   *
   * @returns A new iterator over the server proxy apps.
   */
  running(): IterableIterator<IModel>;

  /**
   * Shut down a proxy app by name.
   *
   * @param name - The name of the proxy app.
   *
   * @returns A promise that resolves when the app is shut down.
   */
  shutdown(name: string): Promise<void>;

  /**
   * Shut down all proxy apps.
   *
   * @returns A promise that resolves when all of the apps are shut down.
   */
  shutdownAll(): Promise<void>;

  /**
   * Force a refresh of the running proxy apps.
   *
   * @returns A promise that with the list of running proxy apps.
   *
   * #### Notes
   * This is not typically meant to be called by the user, since the
   * manager maintains its own internal state.
   */
  refreshRunning(): Promise<void>;
}
