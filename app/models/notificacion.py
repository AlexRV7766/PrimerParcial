from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Notificacion(Base):
    __tablename__ = "notificaciones"

    id = Column(Integer, primary_key=True, index=True)

    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"))
    taller_id = Column(Integer, ForeignKey("taller.id", ondelete="CASCADE"))

    mensaje = Column(Text)
    leido = Column(Boolean, default=False)

    fecha = Column(TIMESTAMP, server_default=func.now())