export type EstadoEmergencia = 'pendiente' | 'en_proceso' | 'atendido' | 'cancelado';

export interface EmergenciaCreate {
  vehiculo_id: number;
  descripcion: string;
  latitud: number;
  longitud: number;
}

export interface EmergenciaResponse {
  id: number;
  descripcion: string;
  latitud: number;
  longitud: number;
  estado: EstadoEmergencia;
  vehiculo_id: number;
}
