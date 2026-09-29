from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth_token import decode_token
from app.core.config import get_db

import app.crud.parametro_medido_crud as crud
import app.schemas.parametro_medido_schema as schemas


app = APIRouter()


@app.get("/list")
def list_parametros(db: Session = Depends(get_db)):
    return crud.get_parametros(db=db)


@app.get(
    "/{parametro_id}", response_model=schemas.ParametroMedidoResponse)
def get_parametro(
    parametro_id: int,
    db: Session = Depends(get_db)
):

    parametro = crud.get_parametro(
        db=db,
        parametro_id=parametro_id
    )

    if parametro is None:
        raise HTTPException(
            status_code=404,
            detail="Parámetro no encontrado"
        )

    return parametro


@app.post(
    "/create", response_model=schemas.ParametroMedidoResponse)
def create_parametro(
    parametro: schemas.ParametroMedidoCreate,
    db: Session = Depends(get_db)
):
    return crud.crear_parametro(
        db=db,
        parametro=parametro
    )


@app.put(
    "/update/{parametro_id}", response_model=schemas.ParametroMedidoResponse)
def update_parametro(
    parametro_id: int,
    parametro: schemas.ParametroMedidoUpdate,
    db: Session = Depends(get_db)
):
    return crud.actualizar_parametro(
        db=db,
        parametro_id=parametro_id,
        parametro=parametro
    )