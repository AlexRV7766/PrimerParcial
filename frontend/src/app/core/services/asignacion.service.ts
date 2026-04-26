import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';

export interface AsignacionResponse {
  id: number;
  emergencia_id: number;
  taller_id: number;
  tecnico_id?: number;
  estado: 'asignado' | 'aceptado' | 'rechazado';
  fecha: string;
}

@Injectable({ providedIn: 'root' })
export class AsignacionService {
  private http = inject(HttpClient);
  private base = `${environment.apiUrl}/asignaciones`;

  miTaller() {
    return this.http.get<AsignacionResponse[]>(`${this.base}/mi-taller`);
  }

  aceptar(asignacionId: number, tecnicoId: number) {
    return this.http.put(`${this.base}/aceptar/${asignacionId}`, { tecnico_id: tecnicoId });
  }

  tomar(emergenciaId: number, tecnicoId: number) {
    return this.http.post(`${this.base}/tomar/${emergenciaId}`, { tecnico_id: tecnicoId });
  }

  rechazar(asignacionId: number) {
    return this.http.put(`${this.base}/rechazar/${asignacionId}`, {});
  }

  asignarTecnico(asignacionId: number, tecnicoId: number) {
    return this.http.put(`${this.base}/asignar-tecnico/${asignacionId}`, { tecnico_id: tecnicoId });
  }
}
