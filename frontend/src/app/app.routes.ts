import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';
import { roleGuard } from './core/guards/role.guard';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  {
    path: 'login',
    loadComponent: () => import('./features/auth/login/login.component').then(m => m.LoginComponent),
  },
  {
    path: 'register',
    loadComponent: () => import('./features/auth/register/register.component').then(m => m.RegisterComponent),
  },
  {
    path: 'dashboard',
    canActivate: [authGuard],
    loadComponent: () => import('./features/dashboard/dashboard.component').then(m => m.DashboardComponent),
  },
  
  // ── RUTAS CLIENTE / COMUNES ──
  {
    path: 'emergencias',
    canActivate: [authGuard],
    children: [
      {
        path: '',
        loadComponent: () => import('./features/emergencias/emergencias-lista/emergencias-lista.component').then(m => m.EmergenciasListaComponent),
      },
      {
        path: 'nueva',
        canActivate: [roleGuard],
        data: { roles: ['cliente'] }, // Solo clientes pueden crear
        loadComponent: () => import('./features/emergencias/emergencia-nueva/emergencia-nueva.component').then(m => m.EmergenciaNuevaComponent),
      },
      {
        path: ':id',
        loadComponent: () => import('./features/emergencias/emergencia-detalle/emergencia-detalle.component').then(m => m.EmergenciaDetalleComponent),
      },
    ],
  },
  {
    path: 'vehiculos',
    canActivate: [authGuard, roleGuard],
    data: { roles: ['cliente'] },
    children: [
      {
        path: '',
        loadComponent: () => import('./features/vehiculos/vehiculos-lista/vehiculos-lista.component').then(m => m.VehiculosListaComponent),
      },
      {
        path: 'nuevo',
        loadComponent: () => import('./features/vehiculos/vehiculo-form/vehiculo-form.component').then(m => m.VehiculoFormComponent),
      },
      {
        path: ':id/editar',
        loadComponent: () => import('./features/vehiculos/vehiculo-form/vehiculo-form.component').then(m => m.VehiculoFormComponent),
      },
    ],
  },
  {
    path: 'talleres',
    canActivate: [authGuard],
    loadComponent: () => import('./features/talleres/talleres-lista.component').then(m => m.TalleresListaComponent),
  },

  // ── RUTAS ADMINISTRADOR ──
  {
    path: 'admin/usuarios',
    canActivate: [authGuard, roleGuard],
    data: { roles: ['administrador'] },
    loadComponent: () => import('./features/admin/admin-usuarios/admin-usuarios.component').then(m => m.AdminUsuariosComponent),
  },

  // ── RUTAS TALLER ──
  {
    path: 'taller',
    canActivate: [authGuard, roleGuard],
    data: { roles: ['taller'] },
    children: [
      {
        path: 'emergencias',
        loadComponent: () => import('./features/taller/taller-emergencias/taller-emergencias.component').then(m => m.TallerEmergenciasComponent),
      },
      {
        path: 'tecnicos',
        loadComponent: () => import('./features/taller/taller-tecnicos/taller-tecnicos.component').then(m => m.TallerTecnicosComponent),
      },
      {
        path: 'perfil',
        loadComponent: () => import('./features/taller/taller-perfil/taller-perfil.component').then(m => m.TallerPerfilComponent),
      },
      {
        path: 'asignaciones', // Por ahora lo mandamos al mismo lugar que emergencias
        redirectTo: 'emergencias',
        pathMatch: 'full'
      }
    ]
  },

  // ── RUTAS TÉCNICO ──
  {
    path: 'tecnico/emergencias',
    canActivate: [authGuard, roleGuard],
    data: { roles: ['tecnico'] },
    loadComponent: () => import('./features/tecnico/tecnico-emergencias/tecnico-emergencias.component').then(m => m.TecnicoEmergenciasComponent),
  },

  { path: '**', redirectTo: 'dashboard' },
];

