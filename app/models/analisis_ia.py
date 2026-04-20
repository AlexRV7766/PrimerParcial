from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class AnalisisIA(Base):
    __tablename__ = "analisis_ia"

    id = Column(Integer, primary_key=True, index=True)

    emergencia_id = Column(Integer, ForeignKey("emergencia.id", ondelete="CASCADE"))

    transcripcion = Column(Text)
    clasificacion = Column(String(50))
    resumen = Column(Text)

    confianza = Column(Float)

    creado_en = Column(TIMESTAMP, server_default=func.now())

    emergencia = relationship("Emergencia", back_populates="analisis")