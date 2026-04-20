from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from app.core.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))
    telefono = Column(String(20))
    rol = Column(String(20), default="cliente")
    activo = Column(Boolean, default=True)
    creado_en = Column(TIMESTAMP, server_default=func.now())

    vehiculos = relationship("Vehiculo", back_populates="usuario")
    emergencias = relationship("Emergencia", back_populates="usuario")