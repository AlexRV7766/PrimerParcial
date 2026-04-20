from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Ubicacion(Base):
    __tablename__ = "ubicaciones"

    id = Column(Integer, primary_key=True, index=True)

    emergencia_id = Column(Integer, ForeignKey("emergencia.id", ondelete="CASCADE"))

    latitud = Column(DECIMAL(9,6))
    longitud = Column(DECIMAL(9,6))

    fecha = Column(TIMESTAMP, server_default=func.now())

    emergencia = relationship("Emergencia", back_populates="ubicaciones")