from sqlalchemy.orm import Session
from app.models.vehiculo import Vehiculo

def crear_vehiculo(db: Session, data, usuario_id: int):
    vehiculo = Vehiculo(
        usuario_id=usuario_id,
        marca=data.marca,
        modelo=data.modelo,
        placa=data.placa,
        anio=data.anio
    )
    db.add(vehiculo)
    db.commit()
    db.refresh(vehiculo)
    return vehiculo


def obtener_vehiculos(db: Session, usuario_id: int):
    return db.query(Vehiculo).filter(Vehiculo.usuario_id == usuario_id).all()


def obtener_vehiculo(db: Session, vehiculo_id: int, usuario_id: int):
    return db.query(Vehiculo).filter(
        Vehiculo.id == vehiculo_id,
        Vehiculo.usuario_id == usuario_id
    ).first()


def actualizar_vehiculo(db: Session, vehiculo, data):
    vehiculo.marca = data.marca
    vehiculo.modelo = data.modelo
    vehiculo.placa = data.placa
    vehiculo.anio = data.anio

    db.commit()
    db.refresh(vehiculo)
    return vehiculo


def eliminar_vehiculo(db: Session, vehiculo):
    db.delete(vehiculo)
    db.commit()