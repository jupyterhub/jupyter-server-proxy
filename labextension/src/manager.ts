import { Signal, ISignal } from "@lumino/signaling";
import { Poll } from "@lumino/polling";
import { ISettingRegistry } from "@jupyterlab/settingregistry";
import { ServerConnection, BaseManager } from "@jupyterlab/services";
import { TranslationBundle } from "@jupyterlab/translation";
import { listRunning, shutdown } from "./restapi";
import * as ServerProxyApp from "./serverproxy";

// Default refresh interval (in milliseconds) for polling
const DEFAULT_REFRESH_INTERVAL = 10000; // ms

/**
 * A server proxy manager.
 */
export class ServerProxyManager extends BaseManager implements ServerProxyApp.IManager {
  /**
   * Construct a new server proxy manager.
   */
  constructor(options: ServerProxyManager.IOptions) {
    super(options);
    this._trans = options.trans;
    this._settings = options.settings || null;

    const interval =
      (this._settings?.get("refreshInterval").composite as number) ||
      DEFAULT_REFRESH_INTERVAL;

    // Start polling with exponential backoff.
    this._proxyPoll = new Poll({
      auto: false,
      factory: () => this.requestRunning(),
      frequency: {
        interval: interval,
        backoff: true,
        max: 300 * 1000,
      },
      name: `@jupyterhub/jupyter-server-proxy:Manager#models`,
      standby: options.standby ?? "when-hidden",
    });

    // Initialize internal data.
    this._ready = (async () => {
      await this!._proxyPoll.start();
      await this!._proxyPoll.tick;
      this._isReady = true;
    })();

    // Fire callback when settings are changed
    if (this._settings) {
      this._settings?.changed.connect(this._onSettingsChange, this);
      this._onSettingsChange(this._settings);
    }
  }

  /**
   * Test whether the manager is ready.
   */
  get isReady(): boolean {
    return this._isReady;
  }

  /**
   * A promise that fulfills when the manager is ready.
   */
  get ready(): Promise<void> {
    return this._ready;
  }

  /**
   * A signal emitted when the running server proxies change.
   */
  get runningChanged(): ISignal<this, ServerProxyApp.IModel[]> {
    return this._runningChanged;
  }

  /**
   * A signal emitted when there is a connection failure.
   */
  get connectionFailure(): ISignal<this, Error> {
    return this._connectionFailure;
  }

  /**
   * Dispose of the resources used by the manager.
   */
  dispose(): void {
    if (this.isDisposed) {
      return;
    }
    this._proxyPoll.dispose();
    this._settings?.changed.disconnect(this._onSettingsChange, this);
    super.dispose();
  }

  /**
   * Create an iterator over the most recent running proxy apps.
   *
   * @returns A new iterator over the running proxy apps.
   */
  running(): IterableIterator<ServerProxyApp.IModel> {
    return this._models[Symbol.iterator]();
  }

  /**
   * Shut down a server proxy app by name.
   */
  async shutdown(name: string): Promise<void> {
    await shutdown(name, this._trans, this.serverSettings);
    await this.refreshRunning();
  }

  /**
   * Shut down all server proxy apps.
   *
   * @returns A promise that resolves when all of the apps are shut down.
   */
  async shutdownAll(): Promise<void> {
    // Update the list of models to make sure our list is current.
    await this.refreshRunning();

    // Shut down all models.
    await Promise.all(
      this._names.map((name) =>
        shutdown(name, this._trans, this.serverSettings)
      )
    );

    // Update the list of models to clear out our state.
    await this.refreshRunning();
  }

  /**
   * Force a refresh of the running server proxy apps.
   *
   * @returns A promise that with the list of running proxy apps.
   */
  async refreshRunning(): Promise<void> {
    await this._proxyPoll.refresh();
    await this._proxyPoll.tick;
  }

  /**
   * Refresh the running proxy apps.
   */
  protected async requestRunning(): Promise<void> {
    let models: ServerProxyApp.IModel[];
    try {
      models = await listRunning(this.serverSettings);
    } catch (err: any) {
      // Handle network errors, as well as cases where we are on a
      // JupyterHub and the server is not running. JupyterHub returns a
      // 503 (<2.0) or 424 (>2.0) in that case.
      if (
        err instanceof ServerConnection.NetworkError ||
        err.response?.status === 503 ||
        err.response?.status === 424
      ) {
        this._connectionFailure.emit(err);
      }
      throw err;
    }

    if (this.isDisposed) {
      return;
    }

    const names = models.map(({ name }) => name).sort();
    if (names === this._names) {
      // Identical models list, so just return
      return;
    }

    this._names = names;
    this._models = models;
    this._runningChanged.emit(this._models);
  }

  /**
   * Callback invoked upon a change to plugin settings.
   *
   * @private
   * @param settings - plugin settings
   */
  private _onSettingsChange(settings: ISettingRegistry.ISettings) {
    this._proxyPoll.frequency = {
      ...this._proxyPoll.frequency,
      interval: settings.composite.refreshInterval as number,
    };
  }

  private _isReady = false;

  private _names: string[] = [];
  private _models: ServerProxyApp.IModel[] = [];
  private _proxyPoll: Poll;
  private _trans: TranslationBundle;
  private _settings: ISettingRegistry.ISettings | null;
  private _ready: Promise<void>;
  private _runningChanged = new Signal<this, ServerProxyApp.IModel[]>(this);
  private _connectionFailure = new Signal<this, Error>(this);
}

/**
 * The namespace for `ServerProxyManager` class statics.
 */
export namespace ServerProxyManager {
  /**
   * The options used to initialize a ServerProxyManager.
   */
  export interface IOptions extends BaseManager.IOptions {
    /**
     * Translation Bundle.
     */
    trans: TranslationBundle;

    /**
     * The currently loaded settings.
     */
    settings?: ISettingRegistry.ISettings;

    /**
     * When the manager stops polling the API. Defaults to `when-hidden`.
     */
    standby?: Poll.Standby | (() => boolean | Poll.Standby);
  }
}
