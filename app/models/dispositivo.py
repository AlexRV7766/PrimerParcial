from sqlalchemy import Column, Integer, Text, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Dispositivo(Base):
    __tablename__ = "dispositivos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"))
    token = Column(Text, unique=True, index=True)
    plataforma = Column(String(20))
    creado_en = Column(DateTime(timezone=True), server_default=func.now())