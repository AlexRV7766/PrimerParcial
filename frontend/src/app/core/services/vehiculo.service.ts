import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { VehiculoCreate, VehiculoResponse } from '../models/vehiculo.model';

@Injectable({ providedIn: 'root' })
export class VehiculoService {
  private http = inject(HttpClient);
  private base = `${environment.apiUrl}/vehiculos`;

  listar() {
    return this.http.get<VehiculoResponse[]>(this.base);
  }

  crear(data: VehiculoCreate) {
    return this.http.post<VehiculoResponse>(this.base, data);
  }

  actualizar(id: number, data: VehiculoCreate) {
    return this.http.put<VehiculoResponse>(`${this.base}/${id}`, data);
  }

  eliminar(id: number) {
    return this.http.delete(`${this.base}/${id}`);
  }
}
