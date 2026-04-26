import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { NavbarComponent } from '../../../shared/navbar/navbar.component';
import { UsuarioService } from '../../../core/services/usuario.service';
import { UsuarioResponse } from '../../../core/models/usuario.model';

@Component({
  selector: 'app-admin-usuarios',
  standalone: true,
  imports: [CommonModule, FormsModule, NavbarComponent],
  templateUrl: './admin-usuarios.component.html',
  styleUrl: './admin-usuarios.component.css',
})
export class AdminUsuariosComponent implements OnInit {
  private usuarioService = inject(UsuarioService);

  usuarios: UsuarioResponse[] = [];
  loading = true;
  mensaje = '';
  error = '';

  readonly ROLES = ['cliente', 'taller', 'tecnico', 'administrador'];

  ngOnInit() { this.cargar(); }

  cargar() {
    this.loading = true;
    this.usuarioService.listar().subscribe({
      next: (data) => { this.usuarios = data; this.loading = false; },
      error: () => { this.error = 'Error al cargar usuarios'; this.loading = false; },
    });
  }

  cambiarRol(usuario: UsuarioResponse, nuevoRol: string) {
    this.mensaje = '';
    this.usuarioService.cambiarRol(usuario.id, nuevoRol).subscribe({
      next: (u) => {
        usuario.rol = u.rol;
        this.mensaje = `Rol de ${u.nombre} actualizado a "${u.rol}"`;
        setTimeout(() => this.mensaje = '', 3000);
      },
      error: (e) => { this.error = e.error?.detail || 'Error al cambiar rol'; },
    });
  }

  // --- MÉTODOS DE EDICIÓN ---
  usuarioEnEdicion: UsuarioResponse | null = null;
  formEdicion = { nombre: '', telefono: '', email: '', activo: true };

  editar(u: UsuarioResponse) {
    this.usuarioEnEdicion = u;
    this.formEdicion = { 
      nombre: u.nombre, 
      telefono: u.telefono, 
      email: u.email, 
      activo: u.activo 
    };
  }

  cancelarEdicion() {
    this.usuarioEnEdicion = null;
  }

  guardarEdicion() {
    if (!this.usuarioEnEdicion) return;
    this.usuarioService.actualizar(this.usuarioEnEdicion.id, this.formEdicion).subscribe({
      next: (u) => {
        this.mensaje = 'Usuario actualizado';
        this.usuarioEnEdicion = null;
        this.cargar();
        setTimeout(() => this.mensaje = '', 3000);
      },
      error: (e) => { this.error = e.error?.detail || 'Error al actualizar'; }
    });
  }

  eliminar(u: UsuarioResponse) {
    if (!confirm(`¿Eliminar al usuario ${u.nombre}?`)) return;
    this.usuarioService.eliminar(u.id).subscribe({
      next: () => {
        this.mensaje = 'Usuario eliminado';
        this.cargar();
        setTimeout(() => this.mensaje = '', 3000);
      },
      error: (e) => { this.error = e.error?.detail || 'Error al eliminar'; }
    });
  }

  rolClass(rol: string): string {
    const map: Record<string, string> = {
      cliente: 'badge-azul',
      taller: 'badge-verde',
      tecnico: 'badge-naranja',
      administrador: 'badge-morado',
    };
    return map[rol] ?? 'badge-gris';
  }
}
