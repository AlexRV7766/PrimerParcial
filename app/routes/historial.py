from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.services.historial_service import obtener_historial

router = APIRouter(prefix="/historial", tags=["Historial"])


@router.get("/{emergencia_id}")
def ver_historial(
    emergencia_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return obtener_historial(db, emergencia_id)