import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { EmergenciaCreate, EmergenciaResponse } from '../models/emergencia.model';

@Injectable({ providedIn: 'root' })
export class EmergenciaService {
  private http = inject(HttpClient);
  private base = `${environment.apiUrl}/emergencias`;

  listar() {
    return this.http.get<EmergenciaResponse[]>(this.base);
  }

  crear(data: EmergenciaCreate) {
    return this.http.post<EmergenciaResponse>(this.base, data);
  }

  cancelar(id: number) {
    return this.http.put<EmergenciaResponse>(`${this.base}/cancelar/${id}`, {});
  }
}
