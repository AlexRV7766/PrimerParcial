import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { EmergenciaService } from '../../../core/services/emergencia.service';
import { EmergenciaResponse } from '../../../core/models/emergencia.model';
import { NavbarComponent } from '../../../shared/navbar/navbar.component';

@Component({
  selector: 'app-emergencias-lista',
  standalone: true,
  imports: [CommonModule, RouterLink, NavbarComponent],
  templateUrl: './emergencias-lista.component.html',
  styleUrl: './emergencias-lista.component.css',
})
export class EmergenciasListaComponent implements OnInit {
  private service = inject(EmergenciaService);
  emergencias: EmergenciaResponse[] = [];
  loading = true;
  mensaje = '';

  ngOnInit() { this.cargar(); }

  cargar() {
    this.loading = true;
    this.service.listar().subscribe({
      next: (data) => { this.emergencias = data; this.loading = false; },
      error: () => { this.loading = false; },
    });
  }

  cancelar(id: number) {
    if (!confirm('¿Cancelar esta emergencia?')) return;
    this.service.cancelar(id).subscribe({
      next: () => { this.mensaje = 'Emergencia cancelada correctamente'; this.cargar(); },
      error: (e) => { this.mensaje = e.error?.detail || 'Error al cancelar'; },
    });
  }

  badgeClass(estado: string): string {
    const map: Record<string, string> = {
      pendiente: 'badge-red',
      en_proceso: 'badge-yellow',
      atendido: 'badge-green',
      cancelado: 'badge-gray',
    };
    return map[estado] ?? 'badge-gray';
  }
}
