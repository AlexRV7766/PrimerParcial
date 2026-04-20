from pydantic import BaseModel

class TecnicoCreate(BaseModel):
    taller_id: int
    nombre: str
    telefono: str


class TecnicoResponse(BaseModel):
    id: int
    nombre: str
    telefono: str
    disponible: bool

    class Config:
        from_attributes = True