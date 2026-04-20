from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class HistorialEstado(Base):
    __tablename__ = "historial_estados"

    id = Column(Integer, primary_key=True, index=True)

    emergencia_id = Column(Integer, ForeignKey("emergencia.id", ondelete="CASCADE"))

    estado = Column(Enum('pendiente','en_proceso','atendido','cancelado', name="estado_historial_enum"))
    fecha = Column(TIMESTAMP, server_default=func.now())

    emergencia = relationship("Emergencia", back_populates="historial")