import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Stats } from '../shared/stats';
import { baseURL } from '../shared/base';
import { Observable } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class StatsService{

  constructor(private http: HttpClient) { }

  getStats(): Observable<Stats[]> {
    return this.http.get<Stats[]>(baseURL + "stats");
  }


}
