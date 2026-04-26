from sqlalchemy.orm import Session
from app.models.emergencia import Emergencia
from app.services.smart_assignment import asignar_taller_inteligente
from app.models.historial_estados import HistorialEstado
import asyncio
from app.services.notificacion_service import crear_notificacion

def crear_emergencia(db: Session, data, usuario_id: int):

    emergencia = Emergencia(
        usuario_id=usuario_id,
        vehiculo_id=data.vehiculo_id,
        descripcion=data.descripcion,
        latitud=data.latitud,
        longitud=data.longitud,
        estado="pendiente"
    )

    db.add(emergencia)
    db.commit()
    db.refresh(emergencia)

    # 🧾 historial inicial
    historial = HistorialEstado(
        emergencia_id=emergencia.id,
        estado="pendiente"
    )

    db.add(historial)
    db.commit()

    # 🚀 asignación automática
    asignacion = asignar_taller_inteligente(db, emergencia)

    # 🔔 NOTIFICACIÓN AL USUARIO (SIEMPRE)
    asyncio.create_task(
        crear_notificacion(
            db,
            usuario_id,
            "🚨 Tu emergencia fue registrada correctamente"
        )
    )

    if asignacion:

        emergencia.estado = "asignado"
        db.commit()

        # 🧾 historial
        historial = HistorialEstado(
            emergencia_id=emergencia.id,
            estado="asignado"
        )
        db.add(historial)
        db.commit()

        # 🔔 notificar taller
        asyncio.create_task(
            crear_notificacion(
                db,
                asignacion.taller_id,
                "🚗 Nueva emergencia asignada"
            )
        )

    else:

        # 🔔 no hay taller
        asyncio.create_task(
            crear_notificacion(
                db,
                usuario_id,
                "⚠️ No se encontró taller disponible"
            )
        )

    return emergencia

def cancelar_emergencia(db: Session, emergencia, usuario_id: int):

    if emergencia.usuario_id != usuario_id:
        return None

    if emergencia.estado == "atendido":
        return None

    emergencia.estado = "cancelado"
    db.commit()

    # historial
    historial = HistorialEstado(
        emergencia_id=emergencia.id,
        estado="cancelado"
    )

    db.add(historial)
    db.commit()

    # 🔔 notificación
    asyncio.create_task(
        crear_notificacion(
            db,
            usuario_id,
            "❌ Emergencia cancelada correctamente"
        )
    )

    return emergencia

def obtener_emergencias(db: Session, usuario_id: int):
    return db.query(Emergencia).filter(Emergencia.usuario_id == usuario_id).order_by(Emergencia.creado_en.desc()).all()

def obtener_emergencia(db: Session, emergencia_id: int, usuario_id: int):
    return db.query(Emergencia).filter(Emergencia.id == emergencia_id, Emergencia.usuario_id == usuario_id).first()
