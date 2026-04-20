from sqlalchemy.orm import Session
from app.models.dispositivo import Dispositivo

def guardar_dispositivo(db: Session, data):

    # 🔍 evitar duplicados
    existente = db.query(Dispositivo).filter(
        Dispositivo.token == data.token
    ).first()

    if existente:
        return existente

    dispositivo = Dispositivo(
        usuario_id=data.usuario_id,
        token=data.token,
        plataforma=data.plataforma
    )

    db.add(dispositivo)
    db.commit()
    db.refresh(dispositivo)

    return dispositivo