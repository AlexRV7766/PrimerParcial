from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.core.deps import get_db, require_roles, get_current_user
from app.models.usuario import Usuario
from app.models.taller import Taller
from app.models.asignaciones import Asignacion

from app.services.asignacion_service import *

router = APIRouter(prefix="/asignaciones", tags=["Asignaciones"])


class AsignarTecnicoBody(BaseModel):
    tecnico_id: int


# ── ADMIN: Crear asignación (sistema → taller) ───────────────────────────────
@router.post("/")
def crear(
    emergencia_id: int,
    taller_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles("administrador"))
):
    return crear_asignacion(db, emergencia_id, taller_id)


# ── TALLER: Ver asignaciones de su taller ────────────────────────────────────
@router.get("/mi-taller")
def mis_asignaciones(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles("taller"))
):
    taller = db.query(Taller).filter(Taller.usuario_id == current_user.id).first()
    if not taller:
        raise HTTPException(status_code=404, detail="No se encontró el taller asociado a tu cuenta")

    return (
        db.query(Asignacion)
        .filter(Asignacion.taller_id == taller.id)
        .order_by(Asignacion.fecha.desc())
        .all()
    )


# ── TALLER: Aceptar emergencia (elige técnico) ───────────────────────────────
@router.put("/aceptar/{asignacion_id}")
def aceptar(
    asignacion_id: int,
    body: AsignarTecnicoBody,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles("taller"))
):
    asignacion = db.query(Asignacion).filter(Asignacion.id == asignacion_id).first()

    if not asignacion:
        raise HTTPException(status_code=404, detail="No encontrada")

    # Verificar que la asignación pertenece al taller del usuario
    taller = db.query(Taller).filter(Taller.usuario_id == current_user.id).first()
    if not taller or asignacion.taller_id != taller.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para esta asignación")

    return aceptar_asignacion(db, asignacion, body.tecnico_id)


# ── TALLER: Tomar emergencia libre (Crear y aceptar) ─────────────────────────
@router.post("/tomar/{emergencia_id}")
def tomar_emergencia(
    emergencia_id: int,
    body: AsignarTecnicoBody,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles("taller"))
):
    from app.models.emergencia import Emergencia
    emergencia = db.query(Emergencia).filter(Emergencia.id == emergencia_id).first()
    if not emergencia or emergencia.estado != "pendiente":
        raise HTTPException(status_code=400, detail="Emergencia no disponible")

    taller = db.query(Taller).filter(Taller.usuario_id == current_user.id).first()
    if not taller:
        raise HTTPException(status_code=403, detail="No tienes taller asociado")

    # Crear la asignación directamente
    nueva_asignacion = Asignacion(
        emergencia_id=emergencia.id,
        taller_id=taller.id,
        estado="aceptado",
        tecnico_id=body.tecnico_id
    )
    db.add(nueva_asignacion)
    
    # Cambiar estado de la emergencia
    emergencia.estado = "en_proceso"
    
    db.commit()
    db.refresh(nueva_asignacion)
    
    return {"mensaje": "Emergencia tomada exitosamente", "asignacion": nueva_asignacion.id}


# ── TALLER: Rechazar emergencia ───────────────────────────────────────────────
@router.put("/rechazar/{asignacion_id}")
def rechazar(
    asignacion_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles("taller"))
):
    asignacion = db.query(Asignacion).filter(Asignacion.id == asignacion_id).first()

    if not asignacion:
        raise HTTPException(status_code=404, detail="No encontrada")

    taller = db.query(Taller).filter(Taller.usuario_id == current_user.id).first()
    if not taller or asignacion.taller_id != taller.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para esta asignación")

    return rechazar_asignacion(db, asignacion)


# ── TALLER: Re-asignar técnico a una asignación ya aceptada ──────────────────
@router.put("/asignar-tecnico/{asignacion_id}")
def asignar_tecnico(
    asignacion_id: int,
    body: AsignarTecnicoBody,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles("taller"))
):
    asignacion = db.query(Asignacion).filter(Asignacion.id == asignacion_id).first()
    if not asignacion:
        raise HTTPException(status_code=404, detail="No encontrada")

    taller = db.query(Taller).filter(Taller.usuario_id == current_user.id).first()
    if not taller or asignacion.taller_id != taller.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para esta asignación")

    asignacion.tecnico_id = body.tecnico_id
    db.commit()
    db.refresh(asignacion)
    return {"mensaje": "Técnico asignado", "tecnico_id": asignacion.tecnico_id}