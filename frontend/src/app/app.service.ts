import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class AppService {

  url = 'http://localhost:8000';

  constructor(private http: HttpClient) { }

  fetch() {
    return this.http.post(`${this.url}/waluty/fetch`, {});
  }

  getAll(year?: number, month?: number, day?: number) {

    let params = new HttpParams();

    if (year) params = params.set('year', year);
    if (month) params = params.set('month', month);
    if (day) params = params.set('day', day);

    return this.http.get(`${this.url}/waluty`, { params });
  }
}