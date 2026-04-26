export interface TallerResponse {
  id: number;
  nombre: string;
  email: string;
  telefono: string;
  direccion: string;
  activo: boolean;
  latitud?: number;
  longitud?: number;
  usuario_id?: number;
}
