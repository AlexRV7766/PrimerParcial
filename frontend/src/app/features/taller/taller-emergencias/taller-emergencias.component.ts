import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { NavbarComponent } from '../../../shared/navbar/navbar.component';
import { EmergenciaService } from '../../../core/services/emergencia.service';
import { AsignacionService, AsignacionResponse } from '../../../core/services/asignacion.service';
import { TecnicoService, TecnicoResponse } from '../../../core/services/tecnico.service';
import { TallerService } from '../../../core/services/taller.service';
import { EmergenciaResponse } from '../../../core/models/emergencia.model';

@Component({
  selector: 'app-taller-emergencias',
  standalone: true,
  imports: [CommonModule, FormsModule, NavbarComponent, RouterModule],
  templateUrl: './taller-emergencias.component.html',
  styleUrl: './taller-emergencias.component.css',
})
export class TallerEmergenciasComponent implements OnInit {
  private emergenciaService = inject(EmergenciaService);
  private asignacionService = inject(AsignacionService);
  private tecnicoService = inject(TecnicoService);
  private tallerService = inject(TallerService);

  emergenciasDisponibles: EmergenciaResponse[] = [];
  asignaciones: AsignacionResponse[] = [];
  tecnicos: TecnicoResponse[] = [];
  tallerId: number | null = null;

  loading = true;
  mensaje = '';
  error = '';

  // Para el modal de aceptar
  emergenciaSeleccionadaId: number | null = null;
  asignacionSeleccionadaId: number | null = null;
  tecnicoSeleccionadoId: number | null = null;

  ngOnInit() { this.cargar(); }

  cargar() {
    this.loading = true;
    // Cargar taller del usuario
    this.tallerService.miTaller().subscribe({
      next: (taller) => {
        this.tallerId = taller.id;
        this.tecnicoService.listarPorTaller(taller.id).subscribe(t => this.tecnicos = t);
      }
    });

    this.emergenciaService.listarDisponibles().subscribe({
      next: (data) => { this.emergenciasDisponibles = data; this.loading = false; },
      error: () => { this.loading = false; },
    });

    this.asignacionService.miTaller().subscribe({
      next: (data) => this.asignaciones = data,
    });
  }

  abrirAceptar(emergenciaId: number, asignacionId?: number) {
    this.emergenciaSeleccionadaId = emergenciaId;
    this.asignacionSeleccionadaId = asignacionId ?? null;
    this.tecnicoSeleccionadoId = this.tecnicos[0]?.id ?? null;
  }

  confirmarAceptar() {
    if (!this.emergenciaSeleccionadaId || !this.tecnicoSeleccionadoId) return;

    if (this.asignacionSeleccionadaId) {
      // Ya existe asignación, solo se acepta
      this.asignacionService.aceptar(this.asignacionSeleccionadaId, this.tecnicoSeleccionadoId).subscribe({
        next: () => {
          this.mensaje = 'Emergencia aceptada y técnico asignado';
          this.cerrarModal();
          this.cargar();
        },
        error: (e) => { this.error = e.error?.detail || 'Error al aceptar'; },
      });
    } else {
      // No existe asignación, el taller la toma libremente
      this.asignacionService.tomar(this.emergenciaSeleccionadaId, this.tecnicoSeleccionadoId).subscribe({
        next: () => {
          this.mensaje = 'Emergencia tomada exitosamente';
          this.cerrarModal();
          this.cargar();
        },
        error: (e) => { this.error = e.error?.detail || 'Error al tomar emergencia'; },
      });
    }
  }

  cerrarModal() {
    this.emergenciaSeleccionadaId = null;
    this.asignacionSeleccionadaId = null;
    setTimeout(() => this.mensaje = '', 3000);
  }

  rechazar(asignacion: AsignacionResponse) {
    if (!confirm('¿Rechazar esta emergencia?')) return;
    this.asignacionService.rechazar(asignacion.id).subscribe({
      next: () => { this.mensaje = 'Emergencia rechazada'; this.cargar(); },
      error: (e) => { this.error = e.error?.detail || 'Error al rechazar'; },
    });
  }

  reasignarTecnico(asignacion: AsignacionResponse, tecnicoId: number) {
    this.asignacionService.asignarTecnico(asignacion.id, tecnicoId).subscribe({
      next: () => { this.mensaje = 'Técnico reasignado correctamente'; setTimeout(() => this.mensaje = '', 3000); },
      error: (e) => { this.error = e.error?.detail || 'Error al reasignar'; },
    });
  }

  estadoClass(estado: string): string {
    const map: Record<string, string> = {
      asignado: 'badge-yellow', aceptado: 'badge-green', rechazado: 'badge-red',
    };
    return map[estado] ?? 'badge-gray';
  }

  emergenciaClass(estado: string): string {
    const map: Record<string, string> = {
      pendiente: 'badge-red', en_proceso: 'badge-yellow', atendido: 'badge-green', cancelado: 'badge-gray',
    };
    return map[estado] ?? 'badge-gray';
  }

  tieneAsignacion(emergenciaId: number): boolean {
    return this.asignaciones.some(a => a.emergencia_id === emergenciaId);
  }
}
