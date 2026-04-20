from sqlalchemy import Column, Integer, String, Float, TIMESTAMP
from sqlalchemy.sql import func
from app.core.database import Base

class Metrica(Base):
    __tablename__ = "metricas"

    id = Column(Integer, primary_key=True, index=True)

    tipo = Column(String(50))
    valor = Column(Float)

    fecha = Column(TIMESTAMP, server_default=func.now())