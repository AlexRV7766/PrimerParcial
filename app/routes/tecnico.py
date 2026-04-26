from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.tecnico import TecnicoCreate, TecnicoResponse
from app.services.tecnico_service import *
from app.core.deps import get_db, require_roles, get_current_user
from app.models.tecnico import Tecnico
from app.models.usuario import Usuario

router = APIRouter(prefix="/tecnicos", tags=["Tecnicos"])


# ── TALLER: Crear técnico para su taller ─────────────────────────────────────
@router.post("/", response_model=TecnicoResponse)
def crear(
    data: TecnicoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles("taller", "administrador"))
):
    return crear_tecnico(db, data)


# ── TALLER/ADMIN: Listar técnicos de un taller ───────────────────────────────
@router.get("/taller/{taller_id}", response_model=list[TecnicoResponse])
def listar_por_taller(
    taller_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return obtener_tecnicos(db, taller_id)


# ── TÉCNICO: Mi perfil técnico ────────────────────────────────────────────────
@router.get("/mi-perfil", response_model=TecnicoResponse)
def mi_perfil(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles("tecnico"))
):
    tecnico = db.query(Tecnico).filter(Tecnico.usuario_id == current_user.id).first()
    if not tecnico:
        raise HTTPException(status_code=404, detail="No se encontró tu perfil de técnico")
    return tecnico


# ── TALLER/ADMIN: Eliminar técnico ───────────────────────────────────────────
@router.delete("/{tecnico_id}")
def eliminar(
    tecnico_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles("taller", "administrador"))
):
    tecnico = db.query(Tecnico).filter(Tecnico.id == tecnico_id).first()
    if not tecnico:
        raise HTTPException(status_code=404, detail="Técnico no encontrado")
    db.delete(tecnico)
    db.commit()
    return {"mensaje": "Técnico eliminado"}


from app.schemas.tecnico import TecnicoUpdate

# ── TALLER/ADMIN: Actualizar técnico ─────────────────────────────────────────
@router.put("/{tecnico_id}", response_model=TecnicoResponse)
def actualizar(
    tecnico_id: int,
    data: TecnicoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles("taller", "administrador"))
):
    tecnico = db.query(Tecnico).filter(Tecnico.id == tecnico_id).first()
    if not tecnico:
        raise HTTPException(status_code=404, detail="Técnico no encontrado")

    tecnico.nombre = data.nombre
    tecnico.telefono = data.telefono
    tecnico.disponible = data.disponible

    db.commit()
    db.refresh(tecnico)
    return tecnico