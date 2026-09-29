from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.sensor_model import Sensor
from app.models.lote_tierra_model import LoteTierra
from app.models.tipo_sensor_model import TipoSensor

from app.schemas.sensor_schema import (
    SensorCreate,
    SensorUpdate
)


def get_sensores(db: Session):
    return db.query(Sensor).all()


def get_sensor(db: Session, sensor_id: int):
    return db.query(Sensor).filter(
        Sensor.Sensor_Id == sensor_id
    ).first()


def crear_sensor(db: Session, sensor: SensorCreate):

    lote = db.query(LoteTierra).filter(
        LoteTierra.Lote_Id == sensor.Lote_Id
    ).first()

    if not lote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lote no encontrado"
        )

    tipo = db.query(TipoSensor).filter(
        TipoSensor.TipoSensor_Id == sensor.TipoSensor_Id
    ).first()

    if not tipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de sensor no encontrado"
        )

    existente = db.query(Sensor).filter(
        Sensor.Sensor_NumeroSerie == sensor.Sensor_NumeroSerie
    ).first()

    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El número de serie ya está registrado"
        )

    db_sensor = Sensor(
        **sensor.model_dump()
    )

    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)

    return db_sensor


def actualizar_sensor(
    db: Session,
    sensor_id: int,
    sensor: SensorUpdate
):

    db_sensor = get_sensor(db, sensor_id)

    if not db_sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sensor no encontrado"
        )

    datos = sensor.model_dump(exclude_unset=True)

    for campo, valor in datos.items():
        setattr(db_sensor, campo, valor)

    db.commit()
    db.refresh(db_sensor)

    return db_sensor