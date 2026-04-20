from sqlalchemy.orm import Session
from app.models.tecnico import Tecnico

def crear_tecnico(db: Session, data):
    tecnico = Tecnico(**data.dict())
    db.add(tecnico)
    db.commit()
    db.refresh(tecnico)
    return tecnico


def obtener_tecnicos(db: Session, taller_id: int):
    return db.query(Tecnico).filter(Tecnico.taller_id == taller_id).all()


def cambiar_disponibilidad(db: Session, tecnico, estado: bool):
    tecnico.disponible = estado
    db.commit()
    db.refresh(tecnico)
    return tecnico