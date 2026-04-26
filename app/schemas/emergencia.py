from pydantic import BaseModel

class EmergenciaCreate(BaseModel):
    vehiculo_id: int
    descripcion: str
    latitud: float
    longitud: float


class EvidenciaResponse(BaseModel):
    id: int
    tipo: str
    url: str

    class Config:
        from_attributes = True

class EmergenciaResponse(BaseModel):
    id: int
    descripcion: str
    latitud: float
    longitud: float
    estado: str
    evidencias: list[EvidenciaResponse] = []

    class Config:
        from_attributes = True