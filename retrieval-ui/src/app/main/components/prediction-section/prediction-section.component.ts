import { AfterViewInit, Component, ElementRef, Input, ViewChild } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { PredictionModel } from '../../lib/models/prediction.model';
import { PredictionDetailDialogComponent } from '../prediction-detail-dialog/prediction-detail-dialog.component';

@Component({
  selector: 'app-prediction-section',
  templateUrl: './prediction-section.component.html',
  styleUrls: ['./prediction-section.component.scss']
})
export class PredictionSectionComponent implements AfterViewInit {

  _predictedLandmarks: PredictionModel[] = undefined;
  rate = 0;

  @Input() set predictedLandmarks(value: PredictionModel[]) {
    if (value != undefined && value != null && this._predictedLandmarks != value) {
      this.scroll(this.predictionSection?.nativeElement);
    }
    this._predictedLandmarks = value;
  }

  get predictedLandmarks(): PredictionModel[] {
    return this._predictedLandmarks;
  }

  @Input()
  inputImage;

  @ViewChild('prediction') predictionSection: ElementRef;

  constructor(public dialog: MatDialog) { }

  ngAfterViewInit(): void {
    this.scroll(this.predictionSection?.nativeElement);
  }

  scroll(el: HTMLElement) {
    if (el) {
      el.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }

  openDialog(index, landmark) {
    const dialogRef = this.dialog.open(PredictionDetailDialogComponent , {
      data: { count: index+1 }
    });
    let instance = dialogRef.componentInstance;
    instance.landmark = landmark;
  }

}
