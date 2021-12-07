import { HttpClient } from '@angular/common/http';
import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { NetModel } from '../../lib/models/net.model';
import { CustomDialogComponent } from '../../shared/custom-dialog/custom-dialog.component';

@Component({
  selector: 'app-upload-page',
  templateUrl: './upload-page.component.html',
  styleUrls: ['./upload-page.component.scss']
})
export class UploadPageComponent implements OnInit {

  fileName = '';
  models: NetModel[] = [new NetModel({name:"ResNet", description:"Residual Networks, or ResNets, learn residual functions with reference to the layer inputs, instead of learning unreferenced functions."}), new NetModel({name:"EfficientNet", description:"EfficientNet is a convolutional neural network architecture and scaling method that uniformly scales all dimensions of depth/width/resolution using a compound coefficient. "})];
  selectedModel: NetModel = this.models[0];
  getLocation = false;

  constructor(private http: HttpClient, public dialog: MatDialog) { }

  ngOnInit(): void {
  }

  onFileSelected(event) {

    const file: File = event.target.files[0];

    if (file) {

      this.fileName = file.name;

      const formData = new FormData();

      formData.append("thumbnail", file);

      const upload$ = this.http.post("/api/thumbnail-upload", formData);

      upload$.subscribe();
    }
  }


  retrieveImages() {
    if (!this.fileName) {
      const dialogRef = this.dialog.open(CustomDialogComponent, {
        data: { title: "Wrong request", body: "You must upload a photo first!", icon: "error" }
      });
    }
  }

}
