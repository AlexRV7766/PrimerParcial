from sqlalchemy import Column, Integer, String, Text, ForeignKey, DECIMAL, TIMESTAMP, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Emergencia(Base):
    __tablename__ = "emergencia"

    id = Column(Integer, primary_key=True, index=True)

    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"))
    vehiculo_id = Column(Integer, ForeignKey("vehiculo.id", ondelete="SET NULL"))

    descripcion = Column(Text)

    latitud = Column(DECIMAL(9,6))
    longitud = Column(DECIMAL(9,6))

    tipo = Column(Enum('bateria','llanta','choque','motor','otro', name="tipo_enum"))
    prioridad = Column(Enum('baja','media','alta', name="prioridad_enum"))
    estado = Column(Enum('pendiente','en_proceso','atendido','cancelado', name="estado_enum"), default="pendiente")

    creado_en = Column(TIMESTAMP, server_default=func.now())

    usuario = relationship("Usuario", back_populates="emergencias")
    vehiculo = relationship("Vehiculo", back_populates="emergencias")

    evidencias = relationship("Evidencia", back_populates="emergencia")
    historial = relationship("HistorialEstado", back_populates="emergencia")
    asignaciones = relationship("Asignacion", back_populates="emergencia")
    analisis = relationship("AnalisisIA", back_populates="emergencia")
    ubicaciones = relationship("Ubicacion", back_populates="emergencia")