import { Component, Inject, Input } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { PredictionModel } from '../../lib/models/prediction.model';

@Component({
  selector: 'app-prediction-detail-dialog',
  templateUrl: './prediction-detail-dialog.component.html',
  styleUrls: ['./prediction-detail-dialog.component.scss']
})
export class PredictionDetailDialogComponent {

  @Input()
  landmark: PredictionModel;

  constructor(public dialogRef: MatDialogRef<PredictionDetailDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any) { }

}
