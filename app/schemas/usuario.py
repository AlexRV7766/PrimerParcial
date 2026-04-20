from pydantic import BaseModel, EmailStr, Field

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

class Config:
    from_attributes = True