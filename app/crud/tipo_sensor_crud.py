from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.tipo_sensor_model import TipoSensor
from app.schemas.tipo_sensor_schema import (
    TipoSensorCreate,
    TipoSensorUpdate
)


def get_tipos_sensor(db: Session):
    return db.query(TipoSensor).all()


def get_tipo_sensor(db: Session, tipo_sensor_id: int):
    return db.query(TipoSensor).filter(
        TipoSensor.TipoSensor_Id == tipo_sensor_id
    ).first()


def crear_tipo_sensor(db: Session, tipo_sensor: TipoSensorCreate):

    existente = db.query(TipoSensor).filter(
        TipoSensor.TipoSensor_Nombre ==
        tipo_sensor.TipoSensor_Nombre
    ).first()

    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El tipo de sensor ya existe"
        )

    db_tipo = TipoSensor(
        **tipo_sensor.model_dump()
    )

    db.add(db_tipo)
    db.commit()
    db.refresh(db_tipo)

    return db_tipo


def actualizar_tipo_sensor(
    db: Session,
    tipo_sensor_id: int,
    tipo_sensor: TipoSensorUpdate
):

    db_tipo = get_tipo_sensor(db, tipo_sensor_id)

    if not db_tipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de sensor no encontrado"
        )

    datos = tipo_sensor.model_dump(exclude_unset=True)

    for campo, valor in datos.items():
        setattr(db_tipo, campo, valor)

    db.commit()
    db.refresh(db_tipo)

    return db_tipo