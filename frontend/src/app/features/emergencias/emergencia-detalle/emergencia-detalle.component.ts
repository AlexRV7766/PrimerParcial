import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { NavbarComponent } from '../../../shared/navbar/navbar.component';
import { EmergenciaService } from '../../../core/services/emergencia.service';
import { EmergenciaResponse } from '../../../core/models/emergencia.model';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-emergencia-detalle',
  standalone: true,
  imports: [CommonModule, NavbarComponent, RouterModule],
  template: `
    <app-navbar />
    <div class="page">
      <div class="page-header" style="display:flex; justify-content:space-between; align-items:center;">
        <div>
          <h1 class="page-title">
            <span class="material-icons-outlined">info</span>
            Detalle de la Emergencia #{{ emergenciaId }}
          </h1>
          <p class="page-subtitle">Información completa y evidencias</p>
        </div>
        <button class="btn btn-secondary" (click)="volver()">
          <span class="material-icons-outlined">arrow_back</span> Volver
        </button>
      </div>

      @if (loading) {
        <div class="loading">Cargando detalles...</div>
      } @else if (error) {
        <div class="alert alert-error">{{ error }}</div>
      } @else if (emergencia) {
        <div class="detalle-grid">
          <!-- Columna Izquierda: Información -->
          <div class="info-card">
            <h3>Datos de la Solicitud</h3>
            <div class="info-row">
              <strong>Estado:</strong>
              <span class="badge" [class]="'badge-' + emergencia.estado">{{ emergencia.estado }}</span>
            </div>
            <div class="info-row">
              <strong>Descripción:</strong>
              <p>{{ emergencia.descripcion }}</p>
            </div>
            <div class="info-row">
              <strong>ID Vehículo:</strong>
              <span>#{{ emergencia.vehiculo_id }}</span>
            </div>
            <div class="info-row">
              <strong>Ubicación (GPS):</strong>
              <span class="gps-coords">
                <span class="material-icons-outlined">location_on</span>
                {{ emergencia.latitud }}, {{ emergencia.longitud }}
              </span>
            </div>
          </div>

          <!-- Columna Derecha: Evidencias -->
          <div class="info-card">
            <h3>Evidencias Adjuntas</h3>
            @if (!emergencia.evidencias || emergencia.evidencias.length === 0) {
              <div class="empty">No hay fotos o audios adjuntos.</div>
            } @else {
              <div class="evidencias-gallery">
                @for (ev of emergencia.evidencias; track ev.id) {
                  <div class="evidencia-item">
                    @if (ev.tipo === 'imagen' || ev.tipo === 'foto') {
                      <img [src]="ev.url" alt="Evidencia" class="evidencia-img" (click)="abrirImagen(ev.url)">
                    } @else if (ev.tipo === 'audio') {
                      <audio controls [src]="ev.url"></audio>
                    } @else {
                      <a [href]="ev.url" target="_blank" class="btn btn-secondary">Ver {{ ev.tipo }}</a>
                    }
                  </div>
                }
              </div>
            }
          </div>
        </div>
      }
    </div>
  `,
  styles: [`
    .page { padding: 2rem; max-width: 1000px; margin: 0 auto; }
    .page-header { margin-bottom: 2rem; }
    .page-title { display: flex; align-items: center; gap: 0.5rem; font-size: 2rem; color: #1e293b; }
    .page-subtitle { color: #64748b; font-size: 1.1rem; }
    
    .btn { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.5rem 1rem; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 0.9rem; }
    .btn-secondary { background: #e2e8f0; color: #334155; }
    
    .detalle-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }
    @media (max-width: 768px) { .detalle-grid { grid-template-columns: 1fr; } }
    
    .info-card { background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
    .info-card h3 { margin-top: 0; color: #0f172a; margin-bottom: 1.5rem; border-bottom: 1px solid #e2e8f0; padding-bottom: 0.5rem; }
    .info-row { margin-bottom: 1rem; display: flex; flex-direction: column; gap: 0.25rem; }
    .info-row strong { color: #475569; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; }
    
    .badge { display: inline-block; padding: 0.25rem 0.75rem; border-radius: 999px; font-size: 0.875rem; font-weight: 600; text-transform: capitalize; align-self: flex-start; }
    .badge-pendiente { background: #fee2e2; color: #991b1b; }
    .badge-en_proceso { background: #fef3c7; color: #92400e; }
    .badge-atendido { background: #d1fae5; color: #065f46; }
    .badge-cancelado { background: #f1f5f9; color: #475569; }
    
    .gps-coords { display: inline-flex; align-items: center; gap: 0.25rem; font-family: monospace; font-size: 1rem; color: #3b82f6; background: #eff6ff; padding: 0.5rem; border-radius: 6px; }
    
    .evidencias-gallery { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 1rem; }
    .evidencia-img { width: 100%; height: 150px; object-fit: cover; border-radius: 8px; cursor: pointer; transition: transform 0.2s; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .evidencia-img:hover { transform: scale(1.05); }
    .empty { color: #64748b; font-style: italic; }
  `]
})
export class EmergenciaDetalleComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private emergenciaService = inject(EmergenciaService);
  private auth = inject(AuthService);

  emergenciaId: number | null = null;
  emergencia: EmergenciaResponse | null = null;
  loading = true;
  error = '';

  ngOnInit() {
    this.route.paramMap.subscribe(params => {
      const id = params.get('id');
      if (id) {
        this.emergenciaId = +id;
        this.cargarDetalle();
      } else {
        this.error = 'ID de emergencia no válido';
        this.loading = false;
      }
    });
  }

  cargarDetalle() {
    if (!this.emergenciaId) return;
    this.loading = true;
    this.emergenciaService.obtener(this.emergenciaId).subscribe({
      next: (data) => {
        this.emergencia = data;
        this.loading = false;
      },
      error: (e) => {
        this.error = e.error?.detail || 'Error al cargar la emergencia';
        this.loading = false;
      }
    });
  }

  volver() {
    const rol = this.auth.rol();
    if (rol === 'cliente' || rol === 'administrador') {
      this.router.navigate(['/emergencias']);
    } else if (rol === 'taller') {
      this.router.navigate(['/taller/emergencias']);
    } else if (rol === 'tecnico') {
      this.router.navigate(['/tecnico/emergencias']);
    } else {
      this.router.navigate(['/dashboard']);
    }
  }

  abrirImagen(url: string) {
    window.open(url, '_blank');
  }
}
