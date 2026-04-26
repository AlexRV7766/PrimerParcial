from pydantic import BaseModel, EmailStr, Field
from typing import Literal

ROLES_VALIDOS = Literal["cliente", "taller", "tecnico", "administrador"]

class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)
    telefono: str

class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    email: str
    telefono: str
    rol: str
    activo: bool

    class Config:
        from_attributes = True

class RolUpdate(BaseModel):
    rol: ROLES_VALIDOS

class UsuarioUpdate(BaseModel):
    nombre: str
    telefono: str
    email: EmailStr
    activo: bool