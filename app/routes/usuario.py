from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.services.usuario_service import *
from app.core.deps import get_db
from app.core.deps import get_current_user

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# Crear usuario
@router.post("/", response_model=UsuarioResponse)
def crear(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return crear_usuario(db, usuario)

# Listar usuarios
@router.get("/", response_model=list[UsuarioResponse])
def listar(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return obtener_usuarios(db)

# Obtener uno
@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener(usuario_id: int, db: Session = Depends(get_db)):
    usuario = obtener_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# Eliminar
@router.delete("/{usuario_id}")
def eliminar(usuario_id: int, db: Session = Depends(get_db)):
    usuario = eliminar_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario eliminado"}

# Obtener Usuario autenticado
@router.get("/me", response_model=UsuarioResponse)
def perfil(current_user: Usuario = Depends(get_current_user)):
    return current_user