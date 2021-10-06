import {HttpClient, HttpErrorResponse, HttpEvent} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {catchError, Observable, throwError} from 'rxjs';
import {NetModel} from '../models/net.model';
import {PredictionModel} from '../models/prediction.model';

@Injectable({
  providedIn: 'root'
})
export class LandmarkRetrievalService {
  private _retrievalApiUrl = 'http://127.0.0.1:5000/similar-images';

  constructor(private _httpClient: HttpClient) {
  }

  retrieveSimilarLandmarks(file: File, model: NetModel): Observable<HttpEvent<PredictionModel[]>> {
    const formData = new FormData();
    formData.append("file", file);
    return this._httpClient.post<PredictionModel[]>(`${this._retrievalApiUrl}\\${model.value}`, formData, {
      reportProgress: true,
      observe: 'events',
      responseType: 'json'
    }).pipe(
      catchError(this.handleError)
    );
  }


  private handleError(err: HttpErrorResponse): Observable<never> {
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

}
