from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.taller import TallerCreate, TallerResponse
from app.services.taller_service import *
from app.core.deps import get_db, get_current_user

router = APIRouter(prefix="/talleres", tags=["Talleres"])


@router.post("/", response_model=TallerResponse)
def crear(data: TallerCreate, db: Session = Depends(get_db)):
    return crear_taller(db, data)


@router.get("/", response_model=list[TallerResponse])
def listar(db: Session = Depends(get_db)):
    return obtener_talleres(db)


@router.get("/{taller_id}", response_model=TallerResponse)
def obtener(taller_id: int, db: Session = Depends(get_db)):
    taller = obtener_taller(db, taller_id)

    if not taller:
        raise HTTPException(status_code=404, detail="No encontrado")

    return taller


@router.delete("/{taller_id}")
def eliminar(taller_id: int, db: Session = Depends(get_db)):
    taller = obtener_taller(db, taller_id)

    if not taller:
        raise HTTPException(status_code=404, detail="No encontrado")

    eliminar_taller(db, taller)
    return {"mensaje": "Eliminado"}