from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.emergencia import EmergenciaCreate, EmergenciaResponse
from app.services.emergencia_service import *
from app.core.deps import get_db, get_current_user, require_roles
from app.models.usuario import Usuario
from app.models.emergencia import Emergencia
from app.models.asignaciones import Asignacion
from app.models.tecnico import Tecnico

router = APIRouter(prefix="/emergencias", tags=["Emergencias"])


# ── CLIENTE: Crear emergencia ─────────────────────────────────────────────────
@router.post("/", response_model=EmergenciaResponse)
async def crear(
    data: EmergenciaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles("cliente"))
):
    return crear_emergencia(db, data, current_user.id)


# ── CLIENTE: Listar mis emergencias ──────────────────────────────────────────
@router.get("/mis", response_model=list[EmergenciaResponse])
def listar_mis(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles("cliente"))
):
    return obtener_emergencias(db, current_user.id)


# ── TALLER: Ver emergencias disponibles (pendientes o asignadas a su taller) ─
@router.get("/disponibles", response_model=list[EmergenciaResponse])
def listar_disponibles(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles("taller"))
):
    return (
        db.query(Emergencia)
        .filter(Emergencia.estado == "pendiente")
        .order_by(Emergencia.creado_en.desc())
        .all()
    )


# ── TALLER/ADMIN: Listar todas las emergencias ───────────────────────────────
@router.get("/todas", response_model=list[EmergenciaResponse])
def listar_todas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles("administrador", "taller"))
):
    return db.query(Emergencia).order_by(Emergencia.creado_en.desc()).all()


# ── TÉCNICO: Ver emergencias que tiene asignadas ─────────────────────────────
@router.get("/mis-asignadas", response_model=list[EmergenciaResponse])
def listar_asignadas_tecnico(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles("tecnico"))
):
    # Buscar el técnico asociado a este usuario
    tecnico = db.query(Tecnico).filter(Tecnico.usuario_id == current_user.id).first()
    if not tecnico:
        raise HTTPException(status_code=404, detail="No se encontró tu perfil de técnico")

    asignaciones = (
        db.query(Asignacion)
        .filter(Asignacion.tecnico_id == tecnico.id, Asignacion.estado == "aceptado")
        .all()
    )
    emergencia_ids = [a.emergencia_id for a in asignaciones]
    return db.query(Emergencia).filter(Emergencia.id.in_(emergencia_ids)).all()


# ── GENÉRICO: Obtener detalle de una emergencia ───────────────────────────────
@router.get("/{emergencia_id}", response_model=EmergenciaResponse)
def obtener(
    emergencia_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    if current_user.rol == "cliente":
        emergencia = obtener_emergencia(db, emergencia_id, current_user.id)
    else:
        emergencia = db.query(Emergencia).filter(Emergencia.id == emergencia_id).first()

    if not emergencia:
        raise HTTPException(status_code=404, detail="No encontrada")
    return emergencia


# ── CLIENTE: Cancelar emergencia ──────────────────────────────────────────────
@router.put("/cancelar/{emergencia_id}")
async def cancelar(
    emergencia_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles("cliente"))
):
    emergencia = obtener_emergencia(db, emergencia_id, current_user.id)

    if not emergencia:
        raise HTTPException(status_code=404, detail="No encontrada")

    resultado = cancelar_emergencia(db, emergencia, current_user.id)

    if not resultado:
        raise HTTPException(status_code=400, detail="No se puede cancelar")

    return {"mensaje": "Emergencia cancelada", "estado": resultado.estado}


# ── GENÉRICO: Listar emergencias (compatibilidad hacia atrás) ─────────────────
@router.get("/", response_model=list[EmergenciaResponse])
def listar(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    if current_user.rol == "cliente":
        return obtener_emergencias(db, current_user.id)
    return db.query(Emergencia).order_by(Emergencia.creado_en.desc()).all()