import { Component, inject, OnInit } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { VehiculoService } from '../../../core/services/vehiculo.service';
import { NavbarComponent } from '../../../shared/navbar/navbar.component';

@Component({
  selector: 'app-vehiculo-form',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, RouterLink, NavbarComponent],
  templateUrl: './vehiculo-form.component.html',
  styleUrl: './vehiculo-form.component.css',
})
export class VehiculoFormComponent implements OnInit {
  private fb = inject(FormBuilder);
  private service = inject(VehiculoService);
  private router = inject(Router);
  private route = inject(ActivatedRoute);

  id: number | null = null;
  error = '';
  loading = false;

  form = this.fb.group({
    marca: ['', Validators.required],
    modelo: ['', Validators.required],
    placa: ['', Validators.required],
    anio: [new Date().getFullYear(), [Validators.required, Validators.min(1900), Validators.max(2100)]],
  });

  get isEdit() { return !!this.id; }

  ngOnInit() {
    const idParam = this.route.snapshot.paramMap.get('id');
    if (idParam) {
      this.id = +idParam;
      this.service.listar().subscribe(vehiculos => {
        const v = vehiculos.find(x => x.id === this.id);
        if (v) this.form.patchValue(v);
      });
    }
  }

  submit() {
    if (this.form.invalid) return;
    this.loading = true;
    this.error = '';
    const data = this.form.value as any;
    const obs = this.isEdit ? this.service.actualizar(this.id!, data) : this.service.crear(data);
    obs.subscribe({
      next: () => this.router.navigate(['/vehiculos']),
      error: (e) => {
        this.error = e.error?.detail || 'Error al guardar el vehículo';
        this.loading = false;
      },
    });
  }
}
