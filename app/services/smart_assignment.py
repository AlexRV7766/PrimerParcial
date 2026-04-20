from sqlalchemy.orm import Session
from app.models.taller import Taller
from app.models.tecnico import Tecnico
from app.models.asignaciones import Asignacion
from app.utils.distance import calcular_distancia


def asignar_taller_inteligente(db: Session, emergencia):
    talleres = db.query(Taller).filter(Taller.activo == True).all()

    mejor_taller = None
    mejor_distancia = float("inf")

    # buscar taller más cercano
    for taller in talleres:

        distancia = calcular_distancia(
            emergencia.latitud,
            emergencia.longitud,
            taller.latitud,
            taller.longitud
        )

        # filtrar técnicos disponibles
        tecnicos_disponibles = db.query(Tecnico).filter(
            Tecnico.taller_id == taller.id,
            Tecnico.disponible == True
        ).count()

        if tecnicos_disponibles == 0:
            continue

        # lógica de selección
        if distancia < mejor_distancia:
            mejor_distancia = distancia
            mejor_taller = taller

    # si no hay talleres
    if not mejor_taller:
        return None

    # crear asignación automática
    asignacion = Asignacion(
        emergencia_id=emergencia.id,
        taller_id=mejor_taller.id,
        estado="asignado"
    )

    db.add(asignacion)
    db.commit()
    db.refresh(asignacion)

    return asignacion