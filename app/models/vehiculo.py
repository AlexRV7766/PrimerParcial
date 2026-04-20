from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Vehiculo(Base):
    __tablename__ = "vehiculo"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"))

    marca = Column(String(50))
    modelo = Column(String(50))
    placa = Column(String(20))
    anio = Column(Integer)

    usuario = relationship("Usuario", back_populates="vehiculos")
    emergencias = relationship("Emergencia", back_populates="vehiculo")