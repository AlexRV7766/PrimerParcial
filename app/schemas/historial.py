from pydantic import BaseModel
from datetime import datetime


class HistorialEstadoBase(BaseModel):
    emergencia_id: int
    estado: str


class HistorialEstadoResponse(BaseModel):
    id: int
    emergencia_id: int
    estado: str
    fecha: datetime

    class Config:
        from_attributes = True