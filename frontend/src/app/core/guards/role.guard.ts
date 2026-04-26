import { inject } from '@angular/core';
import { CanActivateFn, Router, ActivatedRouteSnapshot } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const roleGuard: CanActivateFn = (route: ActivatedRouteSnapshot) => {
  const auth = inject(AuthService);
  const router = inject(Router);

  if (!auth.isLoggedIn()) return router.parseUrl('/login');

  const roles: string[] = route.data?.['roles'] ?? [];
  if (roles.length === 0 || auth.hasRole(...roles)) return true;

  // Redirigir al dashboard si no tiene el rol necesario
  return router.parseUrl('/dashboard');
};
