from sqlalchemy.orm import Session
from app.models.asignaciones import Asignacion
from app.models.emergencia import Emergencia
from app.models.tecnico import Tecnico


#  crear asignación inicial (sistema → taller)
def crear_asignacion(db: Session, emergencia_id: int, taller_id: int):
    asignacion = Asignacion(
        emergencia_id=emergencia_id,
        taller_id=taller_id,
        estado="asignado"
    )

    db.add(asignacion)
    db.commit()
    db.refresh(asignacion)

    return asignacion


#  taller acepta emergencia
def aceptar_asignacion(db: Session, asignacion: Asignacion, tecnico_id: int):
    asignacion.estado = "aceptado"
    asignacion.tecnico_id = tecnico_id

    # actualizar emergencia
    emergencia = db.query(Emergencia).filter(Emergencia.id == asignacion.emergencia_id).first()
    emergencia.estado = "en_proceso"

    db.commit()
    db.refresh(asignacion)

    return asignacion


#  rechazar emergencia
def rechazar_asignacion(db: Session, asignacion: Asignacion):
    asignacion.estado = "rechazado"

    # volver a emergencia pendiente
    emergencia = db.query(Emergencia).filter(Emergencia.id == asignacion.emergencia_id).first()
    emergencia.estado = "pendiente"

    db.commit()
    db.refresh(asignacion)

    return asignacion