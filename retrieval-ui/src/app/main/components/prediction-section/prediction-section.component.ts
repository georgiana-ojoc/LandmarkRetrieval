import {AfterViewInit, Component, ElementRef, EventEmitter, Input, Output, ViewChild} from '@angular/core';
import {MatDialog} from '@angular/material/dialog';
import {PredictionModel} from '../../lib/models/prediction.model';
import {PredictionDetailDialogComponent} from '../prediction-detail-dialog/prediction-detail-dialog.component';
import {DetectionModel} from "../../lib/models/detection.model";

@Component({
  selector: 'app-prediction-section',
  templateUrl: './prediction-section.component.html',
  styleUrls: ['./prediction-section.component.scss']
})
export class PredictionSectionComponent implements AfterViewInit {

  rate = 0;
  canRate = true;
  @Input() inputImage = undefined;
  @Input() showDetections = undefined;
  @Output() ratingAdded = new EventEmitter<any>();
  @ViewChild('prediction') predictionSection: ElementRef;
  markers = [];

  constructor(public dialog: MatDialog) {
  }

  _inputDetection: DetectionModel[] = undefined;

  get inputDetection(): DetectionModel[] {
    return this._inputDetection;
  }

  @Input() set inputDetection(inputDetection: DetectionModel[]) {
    this._inputDetection = inputDetection;
    if (this._inputDetection !== undefined && this._inputDetection.length > 0) {
      this.markers.push({
        position: {
          lat: this._inputDetection[0].locations[0].latitude,
          lng: this._inputDetection[0].locations[0].longitude
        },
        title: this._inputDetection[0].name
      });
    }
  }

  _predictedLandmarks: PredictionModel[] = undefined;

  get predictedLandmarks(): PredictionModel[] {
    return this._predictedLandmarks;
  }

  @Input() set predictedLandmarks(predictedLandmarks: PredictionModel[]) {
    if (predictedLandmarks != undefined && this._predictedLandmarks != predictedLandmarks) {
      this.scroll(this.predictionSection?.nativeElement);
      this.canRate = true;
      this.rate = 0;
    }
    this._predictedLandmarks = predictedLandmarks;
    this.markers = [];
  }

  _outputDetections: Map<string, DetectionModel[]> = undefined;

  get outputDetections(): Map<string, DetectionModel[]> {
    if (this._outputDetections !== undefined) {
      for (let detection of this._outputDetections.values()) {
        if (detection.length > 0) {
          this.markers.push({
            position: {
              lat: detection[0].locations[0].latitude,
              lng: detection[0].locations[0].longitude
            },
            title: detection[0].name
          });
        }
      }
    }
    return this._outputDetections;
  }

  @Input() set outputDetections(outputDetections: Map<string, DetectionModel[]>) {
    this._outputDetections = outputDetections;
  }

  ngAfterViewInit(): void {
    this.scroll(this.predictionSection?.nativeElement);
  }

  scroll(el: HTMLElement) {
    if (el) {
      el.scrollIntoView({behavior: "smooth", block: "start"});
    }
  }

  openDialog(index, landmark) {
    const dialogRef = this.dialog.open(PredictionDetailDialogComponent, {
      data: {count: index + 1}
    });
    let instance = dialogRef.componentInstance;
    instance.landmark = landmark;
  }

  onRatingAdd() {
    this.ratingAdded.emit(this.rate);
    this.canRate = false;
  }

}
