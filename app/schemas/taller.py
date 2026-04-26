from pydantic import BaseModel
from typing import Optional

class TallerCreate(BaseModel):
    nombre: str
    email: str
    telefono: str
    direccion: str
    latitud: float
    longitud: float
    usuario_id: Optional[int] = None


class TallerResponse(BaseModel):
    id: int
    nombre: str
    email: str
    telefono: str
    direccion: str
    activo: bool
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    usuario_id: Optional[int] = None

    class Config:
        from_attributes = True

class TallerUpdate(BaseModel):
    nombre: str
    email: str
    telefono: str
    direccion: str
    latitud: float
    longitud: float
    activo: bool