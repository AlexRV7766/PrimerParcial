from sqlalchemy.orm import Session
from app.models.notificacion import Notificacion
from app.core.connection_manager import manager


# guardar en BD + enviar en tiempo real
async def crear_notificacion(db: Session, usuario_id: int, mensaje: str):

    noti = Notificacion(
        usuario_id=usuario_id,
        mensaje=mensaje,
        leido=False
    )

    db.add(noti)
    db.commit()
    db.refresh(noti)

    # enviar en tiempo real
    await manager.send_to_user(usuario_id, mensaje)

    return noti