import {HttpEventType, HttpResponse} from '@angular/common/http';
import {Component, OnInit} from '@angular/core';
import {MatDialog} from '@angular/material/dialog';
import {MatSnackBar} from '@angular/material/snack-bar';
import {DetectionModel} from '../../lib/models/detection.model';
import {NetAccuracyModel} from '../../lib/models/net-accuracy.model';
import {NetModel} from '../../lib/models/net.model';
import {PredictionModel} from '../../lib/models/prediction.model';
import {RatingModel} from '../../lib/models/rating.model';
import {LandmarkDetectionService} from '../../lib/services/landmark-detection.service';
import {LandmarkRetrievalService} from '../../lib/services/landmark-retrieval.service';
import {ModelRatingService} from '../../lib/services/model-rating.service';
import {CustomDialogComponent} from '../../shared/custom-dialog/custom-dialog.component';

@Component({
  selector: 'app-upload-page',
  templateUrl: './upload-page.component.html',
  styleUrls: ['./upload-page.component.scss']
})
export class UploadPageComponent implements OnInit {

  fileName = '';

  models: NetModel[] = [new NetModel({
    name: "ResNet-IBN-GeM",
    value: "resnet-ibn-gem",
    description: "Residual Networks, or ResNets, learn residual functions with reference to the layer inputs, instead of learning unreferenced functions.",
    accuracy: new NetAccuracyModel({train: 96, test: 95, validation: 95})
  }),
    new NetModel({
      name: "EfficientNet",
      value: "efficientnet",
      description: "EfficientNet is a convolutional neural network architecture and scaling method that uniformly scales all dimensions of depth/width/resolution using a compound coefficient.",
      accuracy: new NetAccuracyModel({train: 96, test: 87, validation: 87})
    }),
    new NetModel({
      name: "ResNet-IBN-GeM (training)",
      value: "resnet-ibn-gem-training",
      description: "ResNet-IBN-GeM trained on training set.",
      accuracy: new NetAccuracyModel({train: 85, test: 5.11, validation: NaN})
    }),
    new NetModel({
      name: "ResNet-IBN-GeM (validation)",
      value: "resnet-ibn-gem-validation",
      description: "ResNet-IBN-GeM trained on validation set.",
      accuracy: new NetAccuracyModel({train: NaN, test: 0.61, validation: 90})
    }),
    new NetModel({
      name: "EfficientNet (training)",
      value: "efficientnet-training",
      description: "EfficientNet trained on training set.",
      accuracy: new NetAccuracyModel({train: 99, test: 22.51, validation: NaN})
    }),
    new NetModel({
      name: "EfficientNet (validation)",
      value: "efficientnet-validation",
      description: "EfficientNet trained on validation set.",
      accuracy: new NetAccuracyModel({train: NaN, test: 3.08, validation: 99})
    })];
  selectedModel: NetModel = this.models[0];
  getDetection = false;
  file: File;
  previewFile: string;
  requestProgress: number;
  predictedLandmarks: PredictionModel[] = undefined;
  inputDetection: DetectionModel[] = undefined;
  outputDetections: Map<string, DetectionModel[]> = new Map<string, DetectionModel[]>();

  constructor(
    private retrievalService: LandmarkRetrievalService,
    private modelRatingService: ModelRatingService,
    private detectionService: LandmarkDetectionService,
    private dialog: MatDialog,
    private _snackBar: MatSnackBar
  ) {
  }


  ngOnInit(): void {
    this.initModelRatings();
  }

  onFileSelected(event) {
    this.file = event.target.files[0];

    if (this.file) {
      this.fileName = this.file.name;
      const reader = new FileReader();
      reader.onload = (e: any) => {
        this.previewFile = e.target.result;
      };

      reader.readAsDataURL(this.file);
    }
  }

  initModelRatings() {
    this.models.forEach(model => {

      this.modelRatingService.getAverageRatingsForModel(model).subscribe({
        next: (event: any) => {
          if (event instanceof HttpResponse) {
            model.rating = event.body;
          }
        }
      });

    });
  }

  addRating(score: number) {
    const ratingModel = new RatingModel({score: score, model: this.selectedModel.value});
    this.modelRatingService.postRatingForModel(ratingModel).subscribe({
      next: (event: any) => {
        if (event instanceof HttpResponse) {
          this._snackBar.open("Your rating was added.", "OK");
        }
      },
      error: (_: any) => {
        this._snackBar.open("There was an error and your rating could not be added.", "OK");
      }
    });
  }

  retrieveResults() {
    if (!this.fileName) {
      this.dialog.open(CustomDialogComponent, {
        data: {title: "Invalid request", body: "You must upload an image first.", icon: "error"}
      });
    } else {
      this.retrieveSimilarLandmarks();
      this.retrieveInputLandmark();
    }
  }

  retrieveSimilarLandmarks() {
    this.retrievalService.retrieveSimilarLandmarks(this.file, this.selectedModel).subscribe({
      next: (event: any) => {
        if (event.type === HttpEventType.UploadProgress) {
          this.requestProgress = Math.round((100 * event.loaded) / event.total);
        } else if (event instanceof HttpResponse) {
          this.requestProgress = null;
          this.predictedLandmarks = event.body;
          this.retrieveOutputLandmarks();
        }
      },
      error: (_: any) => {
        console.log("Could not retrieve images for: " + this.fileName);
        this.requestProgress = 0;
      }
    });
  }

  retrieveInputLandmark() {
    if (this.getDetection) {
      this.detectionService.retrieveDetectedLandmark(this.file).subscribe({
        next: (event: any) => {
          if (event instanceof HttpResponse) {
            this.inputDetection = event.body;
          }
        },
        error: (_: any) => {
          console.log("Could not retrieve detected landmark for: " + this.fileName);
        }
      });
    }
  }

  retrieveOutputLandmarks() {
    for (let predictedLandmark of this.predictedLandmarks) {
      let image: string = predictedLandmark.images[0];
      this.detectionService.retrieveDetectedLandmark(image).subscribe({
        next: (event: any) => {
          if (event instanceof HttpResponse) {
            this.outputDetections.set(image, event.body);
          }
        },
        error: (_: any) => {
          console.log("Could not retrieve detected landmark for: " + this.fileName);
        }
      });
    }
  }
}
