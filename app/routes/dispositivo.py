from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.dispositivo import DispositivoCreate
from app.services.dispositivo_service import guardar_dispositivo

router = APIRouter(prefix="/dispositivos", tags=["Dispositivos"])


@router.post("/")
def crear_dispositivo(
    data: DispositivoCreate,
    db: Session = Depends(get_db)
):
    return guardar_dispositivo(db, data)