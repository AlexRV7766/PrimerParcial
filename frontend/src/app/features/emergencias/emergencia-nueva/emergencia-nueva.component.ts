import { Component, inject, OnInit } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { EmergenciaService } from '../../../core/services/emergencia.service';
import { VehiculoService } from '../../../core/services/vehiculo.service';
import { EvidenciaService } from '../../../core/services/evidencia.service';
import { VehiculoResponse } from '../../../core/models/vehiculo.model';
import { NavbarComponent } from '../../../shared/navbar/navbar.component';

@Component({
  selector: 'app-emergencia-nueva',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, RouterLink, NavbarComponent],
  templateUrl: './emergencia-nueva.component.html',
  styleUrl: './emergencia-nueva.component.css',
})
export class EmergenciaNuevaComponent implements OnInit {
  private fb = inject(FormBuilder);
  private emergenciaService = inject(EmergenciaService);
  private vehiculoService = inject(VehiculoService);
  private evidenciaService = inject(EvidenciaService);
  private router = inject(Router);

  vehiculos: VehiculoResponse[] = [];
  error = '';
  loading = false;
  ubicando = false;
  archivoSeleccionado: File | null = null;
  mensaje = '';

  form = this.fb.group({
    vehiculo_id: [null as number | null, Validators.required],
    descripcion: ['', [Validators.required, Validators.minLength(10)]],
    latitud: [null as number | null, Validators.required],
    longitud: [null as number | null, Validators.required],
  });

  ngOnInit() {
    this.vehiculoService.listar().subscribe(v => (this.vehiculos = v));
    this.obtenerUbicacion();
  }

  obtenerUbicacion() {
    if (!navigator.geolocation) return;
    this.ubicando = true;
    navigator.geolocation.getCurrentPosition(
      pos => {
        this.form.patchValue({ latitud: pos.coords.latitude, longitud: pos.coords.longitude });
        this.ubicando = false;
      },
      () => { this.ubicando = false; }
    );
  }

  onFileSelected(event: any) {
    const file: File = event.target.files[0];
    if (file) {
      this.archivoSeleccionado = file;
    }
  }

  submit() {
    if (this.form.invalid) return;
    this.loading = true;
    this.error = '';
    this.mensaje = 'Creando emergencia...';

    this.emergenciaService.crear(this.form.value as any).subscribe({
      next: (emergencia) => {
        if (this.archivoSeleccionado) {
          this.mensaje = 'Subiendo imagen...';
          this.evidenciaService.subirImagen(emergencia.id, this.archivoSeleccionado).subscribe({
            next: () => this.router.navigate(['/emergencias']),
            error: () => {
              // Navegamos de todas formas, la emergencia se creó
              alert('Emergencia creada, pero hubo un error subiendo la imagen.');
              this.router.navigate(['/emergencias']);
            }
          });
        } else {
          this.router.navigate(['/emergencias']);
        }
      },
      error: (e) => {
        this.error = e.error?.detail || 'Error al crear la emergencia';
        this.loading = false;
        this.mensaje = '';
      },
    });
  }
}
