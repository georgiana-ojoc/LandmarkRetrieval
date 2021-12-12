import { AfterViewInit, Component, ElementRef, Input, OnInit, ViewChild } from '@angular/core';
import { PredictionModel } from '../../lib/models/prediction.model';

@Component({
  selector: 'app-prediction-section',
  templateUrl: './prediction-section.component.html',
  styleUrls: ['./prediction-section.component.scss']
})
export class PredictionSectionComponent implements OnInit, AfterViewInit {

  _predictedLandmarks: PredictionModel[] = undefined;

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

  constructor() { }

  ngOnInit() {
  }

  ngAfterViewInit(): void {
    this.scroll(this.predictionSection?.nativeElement);
  }

  scroll(el: HTMLElement) {
    if (el) {
      el.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }

}
