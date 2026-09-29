from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth_token import decode_token
from app.core.config import get_db

import app.crud.tipo_sensor_crud as crud
import app.schemas.tipo_sensor_schema as schemas


app = APIRouter()


@app.get("/list")
def list_tipos_sensor(db: Session = Depends(get_db)):
    return crud.get_tipos_sensor(db=db)


@app.get(
    "/{tipo_sensor_id}", response_model=schemas.TipoSensorResponse)
def get_tipo_sensor(
    tipo_sensor_id: int,
    db: Session = Depends(get_db)
):

    tipo = crud.get_tipo_sensor(
        db=db,
        tipo_sensor_id=tipo_sensor_id
    )

    if tipo is None:
        raise HTTPException(
            status_code=404,
            detail="Tipo de sensor no encontrado"
        )

    return tipo


@app.post(
    "/create", response_model=schemas.TipoSensorResponse)
def create_tipo_sensor(
    tipo_sensor: schemas.TipoSensorCreate,
    db: Session = Depends(get_db)
):
    return crud.crear_tipo_sensor(
        db=db,
        tipo_sensor=tipo_sensor
    )


@app.put(
    "/update/{tipo_sensor_id}", response_model=schemas.TipoSensorResponse)
def update_tipo_sensor(
    tipo_sensor_id: int,
    tipo_sensor: schemas.TipoSensorUpdate,
    db: Session = Depends(get_db)
):
    return crud.actualizar_tipo_sensor(
        db=db,
        tipo_sensor_id=tipo_sensor_id,
        tipo_sensor=tipo_sensor
    )