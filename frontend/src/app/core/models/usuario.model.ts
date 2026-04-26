export interface UsuarioCreate {
  nombre: string;
  email: string;
  password: string;
  telefono: string;
}

export interface UsuarioResponse {
  id: number;
  nombre: string;
  email: string;
  telefono: string;
  rol: string;
}
