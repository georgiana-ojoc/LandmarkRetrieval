import { HttpClient, HttpEventType, HttpResponse } from '@angular/common/http';
import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { NetModel } from '../../lib/models/net.model';
import { PredictionModel } from '../../lib/models/prediction.model';
import { LandmarkRetrievalService } from '../../lib/services/landmark-retrieval.service';
import { CustomDialogComponent } from '../../shared/custom-dialog/custom-dialog.component';

@Component({
  selector: 'app-upload-page',
  templateUrl: './upload-page.component.html',
  styleUrls: ['./upload-page.component.scss']
})
export class UploadPageComponent implements OnInit {

  fileName = '';
  models: NetModel[] = [new NetModel({ name: "ResNet IBN GEM", value: "resnet-ibn-gem", description: "Residual Networks, or ResNets, learn residual functions with reference to the layer inputs, instead of learning unreferenced functions." }),
   new NetModel({ name: "EfficientNet", value: "efficientnet", description: "EfficientNet is a convolutional neural network architecture and scaling method that uniformly scales all dimensions of depth/width/resolution using a compound coefficient. " })];
  selectedModel: NetModel = this.models[0];
  getLocation = false;
  file: File;
  previewFile: string;
  requestProgress: number;
  predictedLandmarks: PredictionModel[] = undefined;


  constructor(private retrievalService: LandmarkRetrievalService, public dialog: MatDialog) { }

  ngOnInit(): void {
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


  retrieveImages() {
    if (!this.fileName) {
      const dialogRef = this.dialog.open(CustomDialogComponent, {
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
          const msg = 'Could not upload the file: ' + this.fileName;
        }
      });
    }
  }

}
