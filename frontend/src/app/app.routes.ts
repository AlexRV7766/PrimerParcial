import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';

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
        loadComponent: () => import('./features/emergencias/emergencia-nueva/emergencia-nueva.component').then(m => m.EmergenciaNuevaComponent),
      },
    ],
  },
  {
    path: 'vehiculos',
    canActivate: [authGuard],
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
  { path: '**', redirectTo: 'dashboard' },
];
