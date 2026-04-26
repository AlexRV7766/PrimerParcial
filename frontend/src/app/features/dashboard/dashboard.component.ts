import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { EmergenciaService } from '../../core/services/emergencia.service';
import { VehiculoService } from '../../core/services/vehiculo.service';
import { EmergenciaResponse } from '../../core/models/emergencia.model';
import { VehiculoResponse } from '../../core/models/vehiculo.model';
import { NavbarComponent } from '../../shared/navbar/navbar.component';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink, NavbarComponent],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css',
})
export class DashboardComponent implements OnInit {
  private emergenciaService = inject(EmergenciaService);
  private vehiculoService = inject(VehiculoService);

  emergencias: EmergenciaResponse[] = [];
  vehiculos: VehiculoResponse[] = [];

  ngOnInit() {
    this.emergenciaService.listar().subscribe(e => (this.emergencias = e));
    this.vehiculoService.listar().subscribe(v => (this.vehiculos = v));
  }

  get pendientes() { return this.emergencias.filter(e => e.estado === 'pendiente').length; }
  get enProceso() { return this.emergencias.filter(e => e.estado === 'en_proceso').length; }
  get atendidas() { return this.emergencias.filter(e => e.estado === 'atendido').length; }

  badgeClass(estado: string): string {
    const map: Record<string, string> = {
      pendiente: 'badge badge-red',
      en_proceso: 'badge badge-yellow',
      atendido: 'badge badge-green',
      cancelado: 'badge badge-gray',
    };
    return map[estado] ?? 'badge badge-gray';
  }
}
