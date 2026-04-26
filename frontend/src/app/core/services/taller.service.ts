import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { TallerResponse } from '../models/taller.model';

@Injectable({ providedIn: 'root' })
export class TallerService {
  private http = inject(HttpClient);
  private base = `${environment.apiUrl}/talleres`;

  listar() {
    return this.http.get<TallerResponse[]>(this.base);
  }
}
