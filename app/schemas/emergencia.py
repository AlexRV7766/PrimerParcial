from pydantic import BaseModel

class EmergenciaCreate(BaseModel):
    vehiculo_id: int
    descripcion: str
    latitud: float
    longitud: float


class EmergenciaResponse(BaseModel):
    id: int
    descripcion: str
    latitud: float
    longitud: float
    estado: str

    class Config:
        from_attributes = True