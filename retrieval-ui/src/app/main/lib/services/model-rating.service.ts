import {HttpClient, HttpErrorResponse, HttpEvent} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {catchError, Observable, throwError} from 'rxjs';
import {NetModel} from '../models/net.model';
import {RatingModel} from "../models/rating.model";

@Injectable({
  providedIn: 'root'
})
export class ModelRatingService {
  private _ratingApiUrl = 'http://127.0.0.1:8080/api/v1/ratings';

  constructor(private _httpClient: HttpClient) {
  }

  getAllRatings(): Observable<HttpEvent<RatingModel[]>> {
    return this._httpClient.get<RatingModel[]>(`${this._ratingApiUrl}/`, {
      reportProgress: true,
      observe: 'events',
      responseType: 'json',
    }).pipe(
      catchError(this.handleError)
    );
  }

  getRatingsForModel(model: NetModel): Observable<HttpEvent<RatingModel[]>> {
    return this._httpClient.get<RatingModel[]>(`${this._ratingApiUrl}/${model.value}`, {
      reportProgress: true,
      observe: 'events',
      responseType: 'json',
    }).pipe(
      catchError(this.handleError)
    );
  }

  getAverageRatingsForModel(model: NetModel): Observable<HttpEvent<number>> {
    return this._httpClient.get<number>(`${this._ratingApiUrl}/${model.value}/average`, {
      reportProgress: true,
      observe: 'events',
      responseType: 'json',
    }).pipe(
      catchError(this.handleError)
    );
  }

  postRatingForModel(model: RatingModel): Observable<HttpEvent<RatingModel>> {
    return this._httpClient.post<RatingModel>(`${this._ratingApiUrl}/`, model, {
      reportProgress: true,
      observe: 'events',
      responseType: 'json',
    }).pipe(
      catchError(this.handleError)
    );
  }

  updateRatingForModel(id: number, model: RatingModel): Observable<HttpEvent<RatingModel>> {
    return this._httpClient.put<RatingModel>(`${this._ratingApiUrl}/${id}`, model, {
      reportProgress: true,
      observe: 'events',
      responseType: 'json',
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
    return throwError(() => new Error(errorMessage));
  }

}
