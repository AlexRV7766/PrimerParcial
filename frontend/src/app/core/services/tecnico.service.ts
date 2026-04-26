import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';

export interface TecnicoResponse {
  id: number;
  taller_id: number;
  nombre: string;
  telefono: string;
  disponible: boolean;
  usuario_id?: number;
}

export interface TecnicoCreate {
  taller_id: number;
  nombre: string;
  telefono: string;
  usuario_id?: number;
}

export interface TecnicoUpdate {
  nombre: string;
  telefono: string;
  disponible: boolean;
}

@Injectable({ providedIn: 'root' })
export class TecnicoService {
  private http = inject(HttpClient);
  private base = `${environment.apiUrl}/tecnicos`;

  listarPorTaller(tallerId: number) {
    return this.http.get<TecnicoResponse[]>(`${this.base}/taller/${tallerId}`);
  }

  crear(data: TecnicoCreate) {
    return this.http.post<TecnicoResponse>(`${this.base}/`, data);
  }

  actualizar(id: number, data: TecnicoUpdate) {
    return this.http.put<TecnicoResponse>(`${this.base}/${id}`, data);
  }

  eliminar(id: number) {
    return this.http.delete(`${this.base}/${id}`);
  }

  miPerfil() {
    return this.http.get<TecnicoResponse>(`${this.base}/mi-perfil`);
  }
}
