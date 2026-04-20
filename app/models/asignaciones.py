from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Asignacion(Base):
    __tablename__ = "asignaciones"

    id = Column(Integer, primary_key=True, index=True)

    emergencia_id = Column(Integer, ForeignKey("emergencia.id", ondelete="CASCADE"))
    taller_id = Column(Integer, ForeignKey("taller.id", ondelete="CASCADE"))
    tecnico_id = Column(Integer, ForeignKey("tecnico.id", ondelete="SET NULL"))

    estado = Column(Enum('asignado','aceptado','rechazado', name="estado_asignacion_enum"))

    fecha = Column(TIMESTAMP, server_default=func.now())

    emergencia = relationship("Emergencia", back_populates="asignaciones")
    taller = relationship("Taller", back_populates="asignaciones")
    tecnico = relationship("Tecnico", back_populates="asignaciones")