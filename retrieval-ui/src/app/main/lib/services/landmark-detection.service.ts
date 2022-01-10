import {HttpClient, HttpErrorResponse, HttpEvent} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {catchError, Observable, throwError} from 'rxjs';
import {DetectionModel} from '../models/detection.model';
import {RemoteFileModel} from "../models/remote-file.model";

@Injectable({
  providedIn: 'root'
})
export class LandmarkDetectionService {

  private _apiUrl = 'http://127.0.0.1:5000/landmark';

  constructor(private _httpClient: HttpClient) {
  }

  private static handleError(err: HttpErrorResponse): Observable<never> {
    let errorMessage = '';
    if (err.error instanceof ErrorEvent) {
      // A client-side or network error occurred. Handle it accordingly.
      errorMessage = `An error occurred: ${err.error.message}`;
    } else {
      // The backend returned an unsuccessful response code.
      errorMessage = `Server returned code: ${err.status}, error message is: ${err.message}`;
    }
    console.error(errorMessage);
    return throwError(errorMessage);
  }

  retrieveDetectedLandmark(file: File | string): Observable<HttpEvent<DetectionModel[]>> {
    let request;
    if (file instanceof File) {
      request = new FormData();
      request.append("file", file);
    } else {
      request = new RemoteFileModel(file);
    }
    return this._httpClient.post<DetectionModel[]>(`${this._apiUrl}`, request, {
      reportProgress: true,
      observe: 'events',
      responseType: 'json'
    }).pipe(
      catchError(LandmarkDetectionService.handleError)
    );
  }
}
