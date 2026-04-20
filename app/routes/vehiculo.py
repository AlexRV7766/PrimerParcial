from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.vehiculo import VehiculoCreate, VehiculoResponse
from app.services.vehiculo_service import *
from app.core.deps import get_db, get_current_user
from app.models.usuario import Usuario

router = APIRouter(prefix="/vehiculos", tags=["Vehiculos"])


# Crear vehículo
@router.post("/", response_model=VehiculoResponse)
def crear(
    data: VehiculoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return crear_vehiculo(db, data, current_user.id)


# Listar mis vehículos
@router.get("/", response_model=list[VehiculoResponse])
def listar(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return obtener_vehiculos(db, current_user.id)


# Obtener uno
@router.get("/{vehiculo_id}", response_model=VehiculoResponse)
def obtener(
    vehiculo_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    vehiculo = obtener_vehiculo(db, vehiculo_id, current_user.id)

    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    return vehiculo


# Actualizar
@router.put("/{vehiculo_id}", response_model=VehiculoResponse)
def actualizar(
    vehiculo_id: int,
    data: VehiculoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    vehiculo = obtener_vehiculo(db, vehiculo_id, current_user.id)

    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    return actualizar_vehiculo(db, vehiculo, data)


# Eliminar
@router.delete("/{vehiculo_id}")
def eliminar(
    vehiculo_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    vehiculo = obtener_vehiculo(db, vehiculo_id, current_user.id)

    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    eliminar_vehiculo(db, vehiculo)

    return {"mensaje": "Vehículo eliminado"}