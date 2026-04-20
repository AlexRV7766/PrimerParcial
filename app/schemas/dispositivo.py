from pydantic import BaseModel

class DispositivoCreate(BaseModel):
    usuario_id: int
    token: str
    plataforma: str