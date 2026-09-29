from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth_token import decode_token
from app.core.config import get_db

import app.crud.sensor_crud as crud
import app.schemas.sensor_schema as schemas


app = APIRouter()


@app.get("/list")
def list_sensores(db: Session = Depends(get_db)):
    return crud.get_sensores(db=db)


@app.get(
    "/{sensor_id}", response_model=schemas.SensorResponse)
def get_sensor(
    sensor_id: int,
    db: Session = Depends(get_db)
):

    sensor = crud.get_sensor(
        db=db,
        sensor_id=sensor_id
    )

    if sensor is None:
        raise HTTPException(
            status_code=404,
            detail="Sensor no encontrado"
        )

    return sensor


@app.post(
    "/create", response_model=schemas.SensorResponse)
def create_sensor(
    sensor: schemas.SensorCreate,
    db: Session = Depends(get_db)
):
    return crud.crear_sensor(
        db=db,
        sensor=sensor
    )


@app.put(
    "/update/{sensor_id}", response_model=schemas.SensorResponse)
def update_sensor(
    sensor_id: int,
    sensor: schemas.SensorUpdate,
    db: Session = Depends(get_db)
):
    return crud.actualizar_sensor(
        db=db,
        sensor_id=sensor_id,
        sensor=sensor
    )