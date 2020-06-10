import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Session } from '../shared/session';
import { baseURL } from '../shared/base';
import { Observable } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class SessionsService {

  constructor(private http: HttpClient) { }

  getSessions(): Observable<Session[]> {
    return this.http.get<Session[]>(baseURL + "sessions");
  }

  resetSessions(): Observable<string> {
    return this.http.post<string>(baseURL + "/reset", "");
  }
}
