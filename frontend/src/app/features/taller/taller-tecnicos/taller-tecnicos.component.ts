import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { NavbarComponent } from '../../../shared/navbar/navbar.component';
import { TecnicoService, TecnicoResponse } from '../../../core/services/tecnico.service';
import { TallerService } from '../../../core/services/taller.service';

@Component({
  selector: 'app-taller-tecnicos',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, NavbarComponent],
  templateUrl: './taller-tecnicos.component.html',
  styleUrl: './taller-tecnicos.component.css',
})
export class TallerTecnicosComponent implements OnInit {
  private tecnicoService = inject(TecnicoService);
  private tallerService = inject(TallerService);
  private fb = inject(FormBuilder);

  tecnicos: TecnicoResponse[] = [];
  tallerId: number | null = null;
  loading = true;
  mensaje = '';
  error = '';

  form = this.fb.group({
    nombre: ['', [Validators.required, Validators.minLength(3)]],
    telefono: ['', Validators.required],
    usuario_id: [null as number | null],
  });

  ngOnInit() {
    this.tallerService.miTaller().subscribe({
      next: (taller) => {
        this.tallerId = taller.id;
        this.cargar();
      },
      error: () => { this.error = 'No se encontró tu taller'; this.loading = false; },
    });
  }

  tecnicoEnEdicion: TecnicoResponse | null = null;

  cargar() {
    if (!this.tallerId) return;
    this.loading = true;
    this.tecnicoService.listarPorTaller(this.tallerId).subscribe({
      next: (data) => { this.tecnicos = data; this.loading = false; },
      error: () => { this.loading = false; },
    });
  }

  editar(t: TecnicoResponse) {
    this.tecnicoEnEdicion = t;
    this.form.patchValue({
      nombre: t.nombre,
      telefono: t.telefono,
      usuario_id: t.usuario_id || null
    });
    // Scroll arriba
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  cancelarEdicion() {
    this.tecnicoEnEdicion = null;
    this.form.reset();
  }

  guardar() {
    if (this.form.invalid || !this.tallerId) return;
    const v = this.form.value;

    if (this.tecnicoEnEdicion) {
      // Actualizar
      this.tecnicoService.actualizar(this.tecnicoEnEdicion.id, {
        nombre: v.nombre!,
        telefono: v.telefono!,
        disponible: this.tecnicoEnEdicion.disponible // Mantiene el estado anterior
      }).subscribe({
        next: () => {
          this.mensaje = 'Técnico actualizado correctamente';
          this.cancelarEdicion();
          this.cargar();
          setTimeout(() => this.mensaje = '', 3000);
        },
        error: (e) => { this.error = e.error?.detail || 'Error al actualizar técnico'; }
      });
    } else {
      // Crear
      this.tecnicoService.crear({
        taller_id: this.tallerId,
        nombre: v.nombre!,
        telefono: v.telefono!,
        usuario_id: v.usuario_id ?? undefined,
      }).subscribe({
        next: () => {
          this.mensaje = 'Técnico agregado correctamente';
          this.form.reset();
          this.cargar();
          setTimeout(() => this.mensaje = '', 3000);
        },
        error: (e) => { this.error = e.error?.detail || 'Error al agregar técnico'; },
      });
    }
  }

  eliminar(id: number) {
    if (!confirm('¿Eliminar este técnico?')) return;
    this.tecnicoService.eliminar(id).subscribe({
      next: () => { this.mensaje = 'Técnico eliminado'; this.cargar(); },
      error: (e) => { this.error = e.error?.detail || 'Error al eliminar'; },
    });
  }
}
