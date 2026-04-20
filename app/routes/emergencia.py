from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.emergencia import EmergenciaCreate, EmergenciaResponse
from app.services.emergencia_service import *
from app.core.deps import get_db, get_current_user
from app.models.usuario import Usuario

router = APIRouter(prefix="/emergencias", tags=["Emergencias"])


# Crear
@router.post("/", response_model=EmergenciaResponse)
def crear(
    data: EmergenciaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return crear_emergencia(db, data, current_user.id)


# Listar
@router.get("/", response_model=list[EmergenciaResponse])
def listar(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return obtener_emergencias(db, current_user.id)


# Obtener una
@router.get("/{emergencia_id}", response_model=EmergenciaResponse)
def obtener(
    emergencia_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    emergencia = obtener_emergencia(db, emergencia_id, current_user.id)

    if not emergencia:
        raise HTTPException(status_code=404, detail="No encontrada")

    return emergencia

@router.put("/cancelar/{emergencia_id}")
def cancelar(
    emergencia_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    emergencia = obtener_emergencia(db, emergencia_id, current_user.id)

    if not emergencia:
        raise HTTPException(status_code=404, detail="No encontrada")

    resultado = cancelar_emergencia(db, emergencia, current_user.id)

    if not resultado:
        raise HTTPException(status_code=400, detail="No se puede cancelar")

    return {"mensaje": "Emergencia cancelada", "estado": resultado.estado}