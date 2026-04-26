import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { UsuarioResponse } from '../models/usuario.model';

@Injectable({ providedIn: 'root' })
export class UsuarioService {
  private http = inject(HttpClient);
  private base = `${environment.apiUrl}/usuarios`;

  listar() {
    return this.http.get<UsuarioResponse[]>(`${this.base}/`);
  }

  cambiarRol(id: number, rol: string) {
    return this.http.put<UsuarioResponse>(`${this.base}/${id}/rol`, { rol });
  }

  actualizar(id: number, data: Partial<UsuarioResponse>) {
    return this.http.put<UsuarioResponse>(`${this.base}/${id}`, data);
  }

  eliminar(id: number) {
    return this.http.delete(`${this.base}/${id}`);
  }
}
