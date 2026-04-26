import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { VehiculoService } from '../../../core/services/vehiculo.service';
import { VehiculoResponse } from '../../../core/models/vehiculo.model';
import { NavbarComponent } from '../../../shared/navbar/navbar.component';

@Component({
  selector: 'app-vehiculos-lista',
  standalone: true,
  imports: [CommonModule, RouterLink, NavbarComponent],
  templateUrl: './vehiculos-lista.component.html',
  styleUrl: './vehiculos-lista.component.css',
})
export class VehiculosListaComponent implements OnInit {
  private service = inject(VehiculoService);
  vehiculos: VehiculoResponse[] = [];
  loading = true;
  mensaje = '';

  ngOnInit() { this.cargar(); }

  cargar() {
    this.loading = true;
    this.service.listar().subscribe({
      next: (data) => { this.vehiculos = data; this.loading = false; },
      error: () => { this.loading = false; },
    });
  }

  eliminar(id: number) {
    if (!confirm('¿Eliminar este vehículo?')) return;
    this.service.eliminar(id).subscribe({
      next: () => { this.mensaje = 'Vehículo eliminado'; this.cargar(); },
      error: (e) => { this.mensaje = e.error?.detail || 'Error al eliminar'; },
    });
  }
}
