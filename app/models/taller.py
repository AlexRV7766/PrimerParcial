from sqlalchemy import Column, Integer, String, Boolean, Text, DECIMAL, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Taller(Base):
    __tablename__ = "taller"

    id = Column(Integer, primary_key=True, index=True)

    nombre = Column(String(100))
    email = Column(String(100))
    telefono = Column(String(20))
    direccion = Column(Text)

    latitud = Column(DECIMAL(9,6))
    longitud = Column(DECIMAL(9,6))

    activo = Column(Boolean, default=True)
    creado_en = Column(TIMESTAMP, server_default=func.now())

    tecnicos = relationship("Tecnico", back_populates="taller")
    asignaciones = relationship("Asignacion", back_populates="taller")