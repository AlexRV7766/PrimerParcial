export interface VehiculoCreate {
  marca: string;
  modelo: string;
  placa: string;
  anio: number;
}

export interface VehiculoResponse {
  id: number;
  marca: string;
  modelo: string;
  placa: string;
  anio: number;
}
