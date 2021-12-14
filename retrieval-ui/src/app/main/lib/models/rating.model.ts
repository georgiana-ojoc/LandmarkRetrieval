export class RatingModel {
  score: number;
  model: string;

  public constructor(init?: Partial<RatingModel>) {
    Object.assign(this, init);
  }
}
