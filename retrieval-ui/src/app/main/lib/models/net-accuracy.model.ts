export class NetAccuracyModel {
  train: number;
  test: number;
  validation: number;

  public constructor(init?: Partial<NetAccuracyModel>) {
    Object.assign(this, init);
  }
}
