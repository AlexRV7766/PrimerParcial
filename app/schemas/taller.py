from pydantic import BaseModel

class TallerCreate(BaseModel):
    nombre: str
    email: str
    telefono: str
    direccion: str
    latitud: float
    longitud: float


class TallerResponse(BaseModel):
    id: int
    nombre: str
    email: str
    telefono: str
    direccion: str
    activo: bool

    class Config:
        from_attributes = True