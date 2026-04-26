import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { NavbarComponent } from '../../../shared/navbar/navbar.component';
import { EmergenciaService } from '../../../core/services/emergencia.service';
import { EmergenciaResponse } from '../../../core/models/emergencia.model';

@Component({
  selector: 'app-tecnico-emergencias',
  standalone: true,
  imports: [CommonModule, NavbarComponent, RouterModule],
  templateUrl: './tecnico-emergencias.component.html',
  styleUrl: './tecnico-emergencias.component.css',
})
export class TecnicoEmergenciasComponent implements OnInit {
  private emergenciaService = inject(EmergenciaService);

  emergencias: EmergenciaResponse[] = [];
  loading = true;
  error = '';

  ngOnInit() {
    this.cargar();
  }

  cargar() {
    this.loading = true;
    this.emergenciaService.listarAsignadas().subscribe({
      next: (data) => { this.emergencias = data; this.loading = false; },
      error: (e) => { this.error = e.error?.detail || 'Error al cargar asignaciones'; this.loading = false; },
    });
  }

  badgeClass(estado: string): string {
    const map: Record<string, string> = {
      pendiente: 'badge-red', en_proceso: 'badge-yellow', atendido: 'badge-green', cancelado: 'badge-gray',
    };
    return map[estado] ?? 'badge-gray';
  }
}
