import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { TallerResponse } from '../models/taller.model';

export interface TallerCreate {
  nombre: string;
  email: string;
  telefono: string;
  direccion: string;
  latitud: number;
  longitud: number;
  usuario_id?: number;
}

export interface TallerUpdate {
  nombre: string;
  email: string;
  telefono: string;
  direccion: string;
  latitud: number;
  longitud: number;
  activo: boolean;
}

@Injectable({ providedIn: 'root' })
export class TallerService {
  private http = inject(HttpClient);
  private base = `${environment.apiUrl}/talleres`;

  listar() {
    return this.http.get<TallerResponse[]>(`${this.base}/`);
  }

  miTaller() {
    return this.http.get<TallerResponse>(`${this.base}/mi-taller`);
  }

  obtener(id: number) {
    return this.http.get<TallerResponse>(`${this.base}/${id}`);
  }

  crear(data: TallerCreate) {
    return this.http.post<TallerResponse>(`${this.base}/`, data);
  }

  actualizar(id: number, data: TallerUpdate) {
    return this.http.put<TallerResponse>(`${this.base}/${id}`, data);
  }

  eliminar(id: number) {
    return this.http.delete(`${this.base}/${id}`);
  }
}

