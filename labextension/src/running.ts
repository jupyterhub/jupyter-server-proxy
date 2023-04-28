import { JupyterFrontEnd } from "@jupyterlab/application";
import { IRunningSessions } from "@jupyterlab/running";
import { LabIcon } from "@jupyterlab/ui-components";
import { ServerProxyManager } from "./manager";
import { IModel as IServerProxyModel } from "./serverproxy";
import serverProxyAppSvgstr from "../style/icons/proxy.svg";

export const ServerProxyAppIcon = new LabIcon({
  name: "server-proxy:proxyAppIcon",
  svgstr: serverProxyAppSvgstr,
});

export namespace CommandIDs {
  export const open = "server-proxy:refresh";
}

export class RunningServerProxyApp implements IRunningSessions.IRunningItem {
  constructor(
    model: IServerProxyModel,
    manager: ServerProxyManager,
    app: JupyterFrontEnd,
  ) {
    this._model = model;
    this._manager = manager;
    this._app = app;
  }
  open(): void {
    this._app.commands.execute(CommandIDs.open, { sp: this._model });
  }
  icon(): LabIcon {
    return ServerProxyAppIcon;
  }
  label(): string {
    return `${this._model.name}`;
  }
  labelTitle(): string {
    return `cmd: ${this._model.cmd}\nport: ${this._model.port}\nunix_socket: ${this._model.unix_socket}\nmanaged: ${this._model.managed}`;
  }
  shutdown(): Promise<void> {
    return this._manager.shutdown(this._model.name);
  }

  private _model: IServerProxyModel;
  private _manager: ServerProxyManager;
  private _app: JupyterFrontEnd;
}
