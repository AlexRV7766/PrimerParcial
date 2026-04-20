from sqlalchemy import Column, Integer, DECIMAL, String, ForeignKey, TIMESTAMP, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Pago(Base):
    __tablename__ = "pago"

    id = Column(Integer, primary_key=True, index=True)

    emergencia_id = Column(Integer, ForeignKey("emergencia.id", ondelete="CASCADE"))

    monto = Column(DECIMAL(10,2))
    metodo = Column(String(50))
    estado = Column(Enum('pendiente','pagado','fallido', name="estado_pago_enum"))

    fecha = Column(TIMESTAMP, server_default=func.now())

    comisiones = relationship("Comision", back_populates="pago")