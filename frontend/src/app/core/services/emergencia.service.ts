import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { EmergenciaCreate, EmergenciaResponse } from '../models/emergencia.model';

@Injectable({ providedIn: 'root' })
export class EmergenciaService {
  private http = inject(HttpClient);
  private base = `${environment.apiUrl}/emergencias`;

  // Cliente: mis emergencias
  listar() {
    return this.http.get<EmergenciaResponse[]>(`${this.base}/`);
  }

  // Taller: emergencias pendientes disponibles
  listarDisponibles() {
    return this.http.get<EmergenciaResponse[]>(`${this.base}/disponibles`);
  }

  // Taller/Admin: todas las emergencias
  listarTodas() {
    return this.http.get<EmergenciaResponse[]>(`${this.base}/todas`);
  }

  // Técnico: emergencias asignadas a él
  listarAsignadas() {
    return this.http.get<EmergenciaResponse[]>(`${this.base}/mis-asignadas`);
  }

  obtener(id: number) {
    return this.http.get<EmergenciaResponse>(`${this.base}/${id}`);
  }

  crear(data: EmergenciaCreate) {
    return this.http.post<EmergenciaResponse>(`${this.base}/`, data);
  }

  cancelar(id: number) {
    return this.http.put<EmergenciaResponse>(`${this.base}/cancelar/${id}`, {});
  }
}

