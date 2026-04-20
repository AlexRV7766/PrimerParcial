from sqlalchemy.orm import Session
from app.models.taller import Taller

def crear_taller(db: Session, data):
    taller = Taller(**data.dict())
    db.add(taller)
    db.commit()
    db.refresh(taller)
    return taller


def obtener_talleres(db: Session):
    return db.query(Taller).all()


def obtener_taller(db: Session, taller_id: int):
    return db.query(Taller).filter(Taller.id == taller_id).first()


def eliminar_taller(db: Session, taller):
    db.delete(taller)
    db.commit()