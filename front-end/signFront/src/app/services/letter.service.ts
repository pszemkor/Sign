import { Injectable } from '@angular/core';
import {baseURL} from '../shared/base'
import { Observable, of } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class LetterService {
  constructor(private http: HttpClient) { }

  getLetterToRecognize(): Observable<string> {
    return this.http.get<string>(baseURL + "currentletter");
  }

}
