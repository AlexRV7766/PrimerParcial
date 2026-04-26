import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { NavbarComponent } from '../../../shared/navbar/navbar.component';
import { TallerService, TallerUpdate } from '../../../core/services/taller.service';
import { TallerResponse } from '../../../core/models/taller.model';

@Component({
  selector: 'app-taller-perfil',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, NavbarComponent],
  template: `
    <app-navbar />
    <div class="page">
      <div class="page-header">
        <h1 class="page-title"><span class="material-icons-outlined">storefront</span> Mi Taller</h1>
        <p class="page-subtitle">Actualiza la información de tu negocio</p>
      </div>

      @if (mensaje) { <div class="alert alert-success">{{ mensaje }}</div> }
      @if (error)   { <div class="alert alert-error">{{ error }}</div> }

      @if (loading) {
        <div class="loading">Cargando...</div>
      } @else if (taller) {
        <div class="form-card">
          <form [formGroup]="form" (ngSubmit)="guardar()" class="form">
            <div class="form-row">
              <div class="form-group">
                <label>Nombre del Taller</label>
                <input type="text" formControlName="nombre">
              </div>
              <div class="form-group">
                <label>Email</label>
                <input type="email" formControlName="email">
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>Teléfono</label>
                <input type="text" formControlName="telefono">
              </div>
              <div class="form-group">
                <label>Dirección</label>
                <input type="text" formControlName="direccion">
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>Latitud</label>
                <input type="number" step="any" formControlName="latitud">
              </div>
              <div class="form-group">
                <label>Longitud</label>
                <input type="number" step="any" formControlName="longitud">
              </div>
            </div>
            <div class="form-group" style="flex-direction:row; align-items:center;">
              <input type="checkbox" formControlName="activo" id="activo" style="width:auto">
              <label for="activo" style="margin-left:0.5rem">Taller Activo (Visible para asignaciones)</label>
            </div>
            
            <button type="submit" class="btn btn-green" [disabled]="form.invalid">
              <span class="material-icons-outlined">save</span> Guardar Cambios
            </button>
          </form>
        </div>
      }
    </div>
  `,
  styles: [`
    .page { padding: 2rem; max-width: 800px; margin: 0 auto; }
    .page-header { margin-bottom: 2rem; }
    .page-title { display: flex; align-items: center; gap: 0.5rem; font-size: 2rem; color: #1e293b; }
    .page-subtitle { color: #64748b; font-size: 1.1rem; }
    .form-card { background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
    .form-row { display: flex; gap: 1rem; margin-bottom: 1rem; }
    .form-group { display: flex; flex-direction: column; flex: 1; }
    .form-group label { font-size: 0.875rem; font-weight: 500; color: #475569; margin-bottom: 0.5rem; }
    .form-group input { padding: 0.75rem; border: 1px solid #cbd5e1; border-radius: 8px; outline: none; }
    .form-group input:focus { border-color: #3b82f6; }
    .btn { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1.5rem; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 1rem; }
    .btn-green { background: #10b981; color: white; margin-top: 1rem; }
    .btn:disabled { opacity: 0.5; cursor: not-allowed; }
    .alert { padding: 1rem; border-radius: 8px; margin-bottom: 1rem; font-weight: 500; }
    .alert-success { background: #d1fae5; color: #065f46; }
    .alert-error { background: #fee2e2; color: #991b1b; }
  `]
})
export class TallerPerfilComponent implements OnInit {
  private tallerService = inject(TallerService);
  private fb = inject(FormBuilder);

  taller: TallerResponse | null = null;
  loading = true;
  mensaje = '';
  error = '';

  form = this.fb.group({
    nombre: ['', Validators.required],
    email: ['', [Validators.required, Validators.email]],
    telefono: ['', Validators.required],
    direccion: ['', Validators.required],
    latitud: [0, Validators.required],
    longitud: [0, Validators.required],
    activo: [true]
  });

  ngOnInit() {
    this.cargar();
  }

  cargar() {
    this.loading = true;
    this.tallerService.miTaller().subscribe({
      next: (data) => {
        this.taller = data;
        this.form.patchValue(data);
        this.loading = false;
      },
      error: () => {
        this.error = 'No se pudo cargar la información de tu taller.';
        this.loading = false;
      }
    });
  }

  guardar() {
    if (this.form.invalid || !this.taller) return;
    const v = this.form.value as TallerUpdate;
    this.tallerService.actualizar(this.taller.id, v).subscribe({
      next: () => {
        this.mensaje = 'Información actualizada correctamente.';
        setTimeout(() => this.mensaje = '', 3000);
      },
      error: (e) => {
        this.error = e.error?.detail || 'Error al actualizar el taller.';
      }
    });
  }
}
