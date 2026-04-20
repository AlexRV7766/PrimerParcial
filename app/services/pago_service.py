from sqlalchemy.orm import Session
from app.models.pago import Pago
from app.models.comisiones import Comision
from app.models.emergencia import Emergencia


def crear_pago(db: Session, emergencia_id: int, monto: float, metodo: str):

    # verificar emergencia
    emergencia = db.query(Emergencia).filter(
        Emergencia.id == emergencia_id
    ).first()

    if not emergencia:
        raise Exception("Emergencia no encontrada")

    # VERIFICAR SI YA EXISTE PAGO (AQUÍ VA)
    pago_existente = db.query(Pago).filter(
        Pago.emergencia_id == emergencia_id
    ).first()

    if pago_existente:
        raise Exception("Esta emergencia ya fue pagada")

    # validar estado de emergencia
    if emergencia.estado != "atendido":
        raise Exception("La emergencia aún no está finalizada")

    # crear pago
    pago = Pago(
        emergencia_id=emergencia_id,
        monto=monto,
        metodo=metodo,
        estado="pagado"
    )

    db.add(pago)
    db.commit()
    db.refresh(pago)

    # comisión
    comision = Comision(
        pago_id=pago.id,
        porcentaje=0.10,
        monto=monto * 0.10
    )

    db.add(comision)

    # confirmar cierre lógico
    emergencia.estado = "atendido"

    db.commit()

    return {
        "mensaje": "Pago realizado con éxito",
        "pago_id": pago.id
    }