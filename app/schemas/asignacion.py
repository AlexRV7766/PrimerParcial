from pydantic import BaseModel

class AsignacionCreate(BaseModel):
    emergencia_id: int
    taller_id: int