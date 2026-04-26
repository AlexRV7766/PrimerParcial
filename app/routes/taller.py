from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.taller import TallerCreate, TallerResponse
from app.services.taller_service import *
from app.core.deps import get_db, get_current_user, require_roles
from app.models.taller import Taller
from app.models.usuario import Usuario

router = APIRouter(prefix="/talleres", tags=["Talleres"])


# ── PÚBLICO: Listar talleres ──────────────────────────────────────────────────
@router.get("/", response_model=list[TallerResponse])
def listar(db: Session = Depends(get_db)):
    return obtener_talleres(db)


# ── TALLER: Ver mi taller ─────────────────────────────────────────────────────
@router.get("/mi-taller", response_model=TallerResponse)
def mi_taller(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles("taller"))
):
    taller = db.query(Taller).filter(Taller.usuario_id == current_user.id).first()
    if not taller:
        raise HTTPException(status_code=404, detail="No se encontró tu taller")
    return taller


# ── PÚBLICO: Obtener un taller ───────────────────────────────────────────────
@router.get("/{taller_id}", response_model=TallerResponse)
def obtener(taller_id: int, db: Session = Depends(get_db)):
    taller = obtener_taller(db, taller_id)
    if not taller:
        raise HTTPException(status_code=404, detail="No encontrado")
    return taller


# ── ADMIN: Crear taller ───────────────────────────────────────────────────────
@router.post("/", response_model=TallerResponse)
def crear(
    data: TallerCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles("administrador"))
):
    return crear_taller(db, data)


# ── ADMIN: Eliminar taller ────────────────────────────────────────────────────
@router.delete("/{taller_id}")
def eliminar(
    taller_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles("administrador"))
):
    taller = obtener_taller(db, taller_id)
    if not taller:
        raise HTTPException(status_code=404, detail="No encontrado")
    eliminar_taller(db, taller)
    return {"mensaje": "Eliminado"}


from app.schemas.taller import TallerUpdate

# ── ADMIN/TALLER: Actualizar taller ──────────────────────────────────────────
@router.put("/{taller_id}", response_model=TallerResponse)
def actualizar(
    taller_id: int,
    data: TallerUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles("administrador", "taller"))
):
    taller = obtener_taller(db, taller_id)
    if not taller:
        raise HTTPException(status_code=404, detail="No encontrado")

    # Si es rol taller, solo puede editar su propio taller
    if current_user.rol == "taller" and taller.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para editar este taller")

    taller.nombre = data.nombre
    taller.email = data.email
    taller.telefono = data.telefono
    taller.direccion = data.direccion
    taller.latitud = data.latitud
    taller.longitud = data.longitud
    taller.activo = data.activo

    db.commit()
    db.refresh(taller)
    return taller