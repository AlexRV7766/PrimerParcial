from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.models.usuario import Usuario
from app.models.asignaciones import Asignacion

from app.services.asignacion_service import *

router = APIRouter(prefix="/asignaciones", tags=["Asignaciones"])


# Crear asignación (sistema → taller)
@router.post("/")
def crear(emergencia_id: int, taller_id: int, db: Session = Depends(get_db)):
    return crear_asignacion(db, emergencia_id, taller_id)


# Taller acepta emergencia
@router.put("/aceptar/{asignacion_id}")
def aceptar(
    asignacion_id: int,
    tecnico_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    asignacion = db.query(Asignacion).filter(Asignacion.id == asignacion_id).first()

    if not asignacion:
        raise HTTPException(status_code=404, detail="No encontrada")

    return aceptar_asignacion(db, asignacion, tecnico_id)


# Taller rechaza emergencia
@router.put("/rechazar/{asignacion_id}")
def rechazar(
    asignacion_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    asignacion = db.query(Asignacion).filter(Asignacion.id == asignacion_id).first()

    if not asignacion:
        raise HTTPException(status_code=404, detail="No encontrada")

    return rechazar_asignacion(db, asignacion)