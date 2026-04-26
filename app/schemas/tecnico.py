from pydantic import BaseModel
from typing import Optional

class TecnicoCreate(BaseModel):
    taller_id: int
    nombre: str
    telefono: str
    usuario_id: Optional[int] = None


class TecnicoResponse(BaseModel):
    id: int
    taller_id: int
    nombre: str
    telefono: str
    disponible: bool
    usuario_id: Optional[int] = None

    class Config:
        from_attributes = True

class TecnicoUpdate(BaseModel):
    nombre: str
    telefono: str
    disponible: bool