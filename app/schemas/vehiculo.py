from pydantic import BaseModel

# Crear
class VehiculoCreate(BaseModel):
    marca: str
    modelo: str
    placa: str
    anio: int

# Respuesta
class VehiculoResponse(BaseModel):
    id: int
    marca: str
    modelo: str
    placa: str
    anio: int

    class Config:
        from_attributes = True