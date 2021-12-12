export class NetModel {
  name: string;
  value: string;
  description: string;
  accuracy: number;

  public constructor(init?: Partial<NetModel>) {
    Object.assign(this, init);
  }
}
