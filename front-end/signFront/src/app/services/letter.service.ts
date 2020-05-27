import { Injectable } from '@angular/core';
import { baseURL } from '../shared/base'
import { Observable, of, interval } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Result } from '../shared/result';

@Injectable({
  providedIn: 'root'
})
export class LetterService {
  constructor(private http: HttpClient) { }

  getLetterToRecognize(): Observable<string> {
    return this.http.get<string>(baseURL + "currentletter");
  }

  checkIfSuccess(): Observable<Result> {
    return this.http.get<Result>(baseURL + "check");
  }

  skipLetter(): Observable<Result> {
    return this.http.post<Result>(baseURL + "skip", null)
  }

}
