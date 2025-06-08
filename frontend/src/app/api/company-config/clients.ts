export {}
// import {Injectable} from '@angular/core';
// import {HttpClient} from '@angular/common/http';
// import {CompanyConfig, ConfigAdapter} from '@api/models';
// import {environment} from '../../../environments/environment';
// import {Observable} from 'rxjs';
// import {map} from 'rxjs/operators';
//
// @Injectable({
//   providedIn: 'root'
// })
// export class ConfigAdminClient {
//   baseUrl = environment.apiUrl + 'admin/configs/';
//
//   constructor(private http: HttpClient,
//               private adapter: ConfigAdapter) {
//   }
//
//   detail(): Observable<CompanyConfig> {
//     return this.http.get<CompanyConfig>(this.baseUrl).pipe(map(this.adapter.adapt));
//   }
//
//   patch(id, model): Observable<CompanyConfig> {
//     return this.http.patch<CompanyConfig>(this.baseUrl, model).pipe(map(this.adapter.adapt));
//   }
// }
