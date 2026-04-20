from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.tecnico import TecnicoCreate, TecnicoResponse
from app.services.tecnico_service import *
from app.core.deps import get_db

router = APIRouter(prefix="/tecnicos", tags=["Tecnicos"])


@router.post("/", response_model=TecnicoResponse)
def crear(data: TecnicoCreate, db: Session = Depends(get_db)):
    return crear_tecnico(db, data)


@router.get("/{taller_id}", response_model=list[TecnicoResponse])
def listar(taller_id: int, db: Session = Depends(get_db)):
    return obtener_tecnicos(db, taller_id)