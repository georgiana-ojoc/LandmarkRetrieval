import { HttpEventType, HttpResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { NetAccuracyModel } from '../../lib/models/net-accuracy.model';
import { NetModel } from '../../lib/models/net.model';
import { PredictionModel } from '../../lib/models/prediction.model';
import { RatingModel } from '../../lib/models/rating.model';
import { LandmarkRetrievalService } from '../../lib/services/landmark-retrieval.service';
import { ModelRatingService } from '../../lib/services/model-rating.service';
import { CustomDialogComponent } from '../../shared/custom-dialog/custom-dialog.component';

@Component({
  selector: 'app-upload-page',
  templateUrl: './upload-page.component.html',
  styleUrls: ['./upload-page.component.scss']
})
export class UploadPageComponent implements OnInit {

  fileName = '';
  models: NetModel[] = [new NetModel({ name: "ResNet IBN GEM", value: "resnet-ibn-gem", description: "Residual Networks, or ResNets, learn residual functions with reference to the layer inputs, instead of learning unreferenced functions.", accuracy: new NetAccuracyModel({train: 96, test: 95, validation: 95}) }),
  new NetModel({ name: "EfficientNet", value: "efficientnet", description: "EfficientNet is a convolutional neural network architecture and scaling method that uniformly scales all dimensions of depth/width/resolution using a compound coefficient. ", accuracy: new NetAccuracyModel({train: 96, test: 87, validation: 87}) })];
  selectedModel: NetModel = this.models[0];
  getLocation = false;
  file: File;
  previewFile: string;
  requestProgress: number;
  predictedLandmarks: PredictionModel[] = undefined;


  constructor(
    private retrievalService: LandmarkRetrievalService,
    private modelRatingService: ModelRatingService,
    private dialog: MatDialog,
    private _snackBar: MatSnackBar
    ) { }


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
    const ratingModel = new RatingModel({ score: score, model: this.selectedModel.value });
    this.modelRatingService.postRatingForModel(ratingModel).subscribe({
      next: (event: any) => {
        if (event instanceof HttpResponse) {
          this._snackBar.open("Your rating was added", "Ok");
        }
      },
      error: (event: any) => {
        this._snackBar.open("There was a error. Your rating could not be added!", "Ok");
      }
    });
  }


  retrieveImages() {
    if (!this.fileName) {
      this.dialog.open(CustomDialogComponent, {
        data: { title: "Wrong request", body: "You must upload a photo first!", icon: "error" }
      });
    }
    else {
      this.retrievalService.retrieveSimilarLandmarks(this.file, this.selectedModel).subscribe({
        next: (event: any) => {
          if (event.type === HttpEventType.UploadProgress) {
            this.requestProgress = Math.round(
              (100 * event.loaded) / event.total);
          }
          else if (event instanceof HttpResponse) {
            this.requestProgress = null;
            this.predictedLandmarks = event.body;
          }
        },
        error: (err: any) => {
          console.log('Could not retrieve images for: ' + this.fileName);
          this.requestProgress = 0;
        }
      });
    }
  }

}
