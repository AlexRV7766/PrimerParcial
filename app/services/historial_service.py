from sqlalchemy.orm import Session
from app.models.historial_estados import HistorialEstado

def registrar_estado(db: Session, emergencia_id: int, estado: str):
    registro = HistorialEstado(
        emergencia_id=emergencia_id,
        estado=estado
    )

    db.add(registro)
    db.commit()
    db.refresh(registro)

    return registro


def obtener_historial(db: Session, emergencia_id: int):
    return db.query(HistorialEstado).filter(
        HistorialEstado.emergencia_id == emergencia_id
    ).order_by(HistorialEstado.fecha.asc()).all()