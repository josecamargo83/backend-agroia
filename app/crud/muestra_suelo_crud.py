from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.muestra_suelo_model import MuestraSuelo
from app.models.sensor_model import Sensor
from app.models.parametro_medido_model import ParametroMedido

from app.schemas.muestra_suelo_schema import (
    MuestraSueloCreate,
    MuestraSueloUpdate
)


def get_muestras(db: Session):
    return db.query(MuestraSuelo).order_by(
        MuestraSuelo.Muestra_FechaHora.desc()
    ).all()


def get_muestra(db: Session, muestra_id: int):
    return db.query(MuestraSuelo).filter(
        MuestraSuelo.Muestra_Id == muestra_id
    ).first()


def crear_muestra(
    db: Session,
    muestra: MuestraSueloCreate
):

    sensor = db.query(Sensor).filter(
        Sensor.Sensor_Id == muestra.Sensor_Id
    ).first()

    if not sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sensor no encontrado"
        )

    parametro = db.query(ParametroMedido).filter(
        ParametroMedido.Parametro_Id == muestra.Parametro_Id
    ).first()

    if not parametro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parámetro no encontrado"
        )

    datos = muestra.model_dump()

    if datos.get("Muestra_FechaHora") is None:
        from datetime import datetime
        datos["Muestra_FechaHora"] = datetime.now()

    db_muestra = MuestraSuelo(**datos)

    db.add(db_muestra)
    db.commit()
    db.refresh(db_muestra)

    return db_muestra


def actualizar_muestra(
    db: Session,
    muestra_id: int,
    muestra: MuestraSueloUpdate
):

    db_muestra = get_muestra(db, muestra_id)

    if not db_muestra:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Muestra no encontrada"
        )

    datos = muestra.model_dump(exclude_unset=True)

    for campo, valor in datos.items():
        setattr(db_muestra, campo, valor)

    db.commit()
    db.refresh(db_muestra)

    return db_muestra