import { HttpClient, HttpErrorResponse, HttpEvent } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { catchError, Observable, throwError } from 'rxjs';
import { LocationModel } from '../models/location.model';

@Injectable({
  providedIn: 'root'
})
export class LandmarkLocationService {

  private _apiUrl = 'http://127.0.0.1:5000/landmark';

  constructor(private _httpClient: HttpClient) { }

  retrieveLandmarkLocation(file: File): Observable<HttpEvent<LocationModel>> {
    const formData = new FormData();
    formData.append("file", file);
    return this._httpClient.post<LocationModel>(`${this._apiUrl}`, formData, {
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
