from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Tecnico(Base):
    __tablename__ = "tecnico"

    id = Column(Integer, primary_key=True, index=True)
    taller_id = Column(Integer, ForeignKey("taller.id", ondelete="CASCADE"))

    nombre = Column(String(100))
    telefono = Column(String(20))
    disponible = Column(Boolean, default=True)

    taller = relationship("Taller", back_populates="tecnicos")
    asignaciones = relationship("Asignacion", back_populates="tecnico")