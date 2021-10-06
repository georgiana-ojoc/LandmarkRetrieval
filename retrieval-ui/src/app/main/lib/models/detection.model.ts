import {LocationModel} from "./location.model";

export class DetectionModel {
  locations: LocationModel[];
  name: string;
  score: number;
}
