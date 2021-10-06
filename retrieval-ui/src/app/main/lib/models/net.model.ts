import {NetAccuracyModel} from "./net-accuracy.model";

export class NetModel {
  name: string;
  value: string;
  description: string;
  rating = 0.0;
  accuracy: NetAccuracyModel;

  public constructor(init?: Partial<NetModel>) {
    Object.assign(this, init);
  }
}
