from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, RolUpdate
from app.services.usuario_service import *
from app.core.deps import get_db, get_current_user, require_roles
from app.models.usuario import Usuario

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


# Obtener usuario autenticado (debe ir ANTES de /{usuario_id})
@router.get("/me", response_model=UsuarioResponse)
def perfil(current_user: Usuario = Depends(get_current_user)):
    return current_user


# Crear usuario (registro público)
@router.post("/", response_model=UsuarioResponse)
def crear(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return crear_usuario(db, usuario)


# Listar usuarios — solo administradores
@router.get("/", response_model=list[UsuarioResponse])
def listar(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles("administrador"))
):
    return obtener_usuarios(db)


# Obtener uno
@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener(usuario_id: int, db: Session = Depends(get_db)):
    usuario = obtener_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


# Cambiar rol — solo administradores
@router.put("/{usuario_id}/rol", response_model=UsuarioResponse)
def cambiar_rol(
    usuario_id: int,
    body: RolUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles("administrador"))
):
    usuario = obtener_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.rol = body.rol
    db.commit()
    db.refresh(usuario)
    return usuario


from app.schemas.usuario import UsuarioUpdate

# Actualizar datos básicos — solo administradores
@router.put("/{usuario_id}", response_model=UsuarioResponse)
def actualizar(
    usuario_id: int,
    body: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles("administrador"))
):
    usuario = obtener_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    usuario.nombre = body.nombre
    usuario.telefono = body.telefono
    usuario.email = body.email
    usuario.activo = body.activo
    
    db.commit()
    db.refresh(usuario)
    return usuario


# Eliminar — solo administradores
@router.delete("/{usuario_id}")
def eliminar(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles("administrador"))
):
    usuario = eliminar_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario eliminado"}