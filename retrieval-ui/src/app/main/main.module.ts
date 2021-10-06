import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {UploadPageComponent} from './components/upload-page/upload-page.component';
import {MainRoutingModule} from './main-routing.module';
import {MaterialModule} from '../helpers/material.module';
import {CustomDialogComponent} from './shared/custom-dialog/custom-dialog.component';
import {FormsModule} from '@angular/forms';
import {PredictionSectionComponent} from './components/prediction-section/prediction-section.component';
import {
  PredictionDetailDialogComponent
} from './components/prediction-detail-dialog/prediction-detail-dialog.component';
import {GoogleMapsModule} from "@angular/google-maps";

@NgModule({
  imports: [
    CommonModule,
    MainRoutingModule,
    MaterialModule,
    FormsModule,
    GoogleMapsModule
  ],
  declarations: [
    UploadPageComponent,
    CustomDialogComponent,
    PredictionSectionComponent,
    PredictionDetailDialogComponent
  ]
})
export class MainModule {
}
