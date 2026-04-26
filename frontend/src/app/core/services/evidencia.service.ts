import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class EvidenciaService {
  private http = inject(HttpClient);
  private base = `${environment.apiUrl}/evidencias`;

  subirImagen(emergenciaId: number, archivo: File) {
    const formData = new FormData();
    formData.append('archivo', archivo);
    return this.http.post(
      `${this.base}/upload?emergencia_id=${emergenciaId}&tipo=imagen`,
      formData
    );
  }
}
