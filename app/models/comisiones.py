from sqlalchemy import Column, Integer, DECIMAL, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Comision(Base):
    __tablename__ = "comisiones"

    id = Column(Integer, primary_key=True, index=True)

    pago_id = Column(Integer, ForeignKey("pago.id", ondelete="CASCADE"))

    porcentaje = Column(DECIMAL(5,2), default=0.10)
    monto = Column(DECIMAL(10,2))

    fecha = Column(TIMESTAMP, server_default=func.now())

    pago = relationship("Pago", back_populates="comisiones")