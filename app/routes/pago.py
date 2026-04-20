from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.services.pago_service import crear_pago

router = APIRouter(prefix="/pagos", tags=["Pagos"])


@router.post("/")
def pagar(
    emergencia_id: int,
    monto: float,
    metodo: str,
    db: Session = Depends(get_db)
):
    return crear_pago(db, emergencia_id, monto, metodo)