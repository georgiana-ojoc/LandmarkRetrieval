import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UploadPageComponent } from './components/upload-page/upload-page.component';
import { MainRoutingModule } from './main-routing.module';
import { MaterialModule } from '../helpers/material.module';
import { CustomDialogComponent } from './shared/custom-dialog/custom-dialog.component';
import { FormsModule } from '@angular/forms';

@NgModule({
  imports: [
    CommonModule,
    MainRoutingModule,
    MaterialModule,
    FormsModule
  ],
  declarations: [
    UploadPageComponent,
    CustomDialogComponent
  ]
})
export class MainModule { }