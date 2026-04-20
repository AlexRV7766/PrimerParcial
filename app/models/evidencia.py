from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Evidencia(Base):
    __tablename__ = "evidencia"

    id = Column(Integer, primary_key=True, index=True)

    emergencia_id = Column(Integer, ForeignKey("emergencia.id", ondelete="CASCADE"))

    tipo = Column(Enum('imagen','audio','texto', name="tipo_evidencia_enum"))
    url = Column(Text)

    creado_en = Column(TIMESTAMP, server_default=func.now())

    emergencia = relationship("Emergencia", back_populates="evidencias")