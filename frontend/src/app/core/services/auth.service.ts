import { Injectable, inject, signal, computed } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { tap } from 'rxjs';
import { environment } from '../../../environments/environment';
import { LoginRequest, TokenResponse } from '../models/auth.model';
import { UsuarioCreate, UsuarioResponse } from '../models/usuario.model';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private http = inject(HttpClient);
  private router = inject(Router);
  private readonly TOKEN_KEY = 'access_token';

  // Signal reactivo con los datos del usuario decodificados del JWT
  private _payload = signal<Record<string, any> | null>(this.decodeToken());

  rol = computed(() => this._payload()?.['rol'] ?? null);
  userId = computed(() => this._payload()?.['sub'] ? parseInt(this._payload()!['sub']) : null);
  email = computed(() => this._payload()?.['email'] ?? null);

  isLoggedIn(): boolean {
    return !!localStorage.getItem(this.TOKEN_KEY);
  }

  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  hasRole(...roles: string[]): boolean {
    return roles.includes(this.rol() ?? '');
  }

  login(data: LoginRequest) {
    return this.http.post<TokenResponse>(`${environment.apiUrl}/auth/login`, data).pipe(
      tap(res => {
        localStorage.setItem(this.TOKEN_KEY, res.access_token);
        this._payload.set(this.decodeToken());
      })
    );
  }

  register(data: UsuarioCreate) {
    return this.http.post<UsuarioResponse>(`${environment.apiUrl}/usuarios/`, data);
  }

  logout() {
    localStorage.removeItem(this.TOKEN_KEY);
    this._payload.set(null);
    this.router.navigate(['/login']);
  }

  private decodeToken(): Record<string, any> | null {
    const token = localStorage.getItem(this.TOKEN_KEY);
    if (!token) return null;
    try {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      return JSON.parse(atob(base64));
    } catch {
      return null;
    }
  }
}

