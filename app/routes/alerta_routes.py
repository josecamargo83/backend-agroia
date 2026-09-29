from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth_token import decode_token
from app.core.config import get_db

import app.crud.alerta_crud as crud
import app.schemas.alerta_schema as schemas


app = APIRouter()


@app.get("/list")
def list_alertas(db: Session = Depends(get_db)):

    return crud.get_alertas(db=db)


@app.get("/{alerta_id}", response_model=schemas.AlertaResponse)
def get_alerta(
    alerta_id: int,
    db: Session = Depends(get_db)
):

    alerta = crud.get_alerta(
        db=db,
        alerta_id=alerta_id
    )

    if alerta is None:
        raise HTTPException(
            status_code=404,
            detail="Alerta no encontrada"
        )

    return alerta


@app.post("/create", response_model=schemas.AlertaResponse)
def create_alerta(
    alerta: schemas.AlertaCreate,
    db: Session = Depends(get_db)
):

    return crud.crear_alerta(
        db=db,
        alerta=alerta
    )


@app.put("/update/{alerta_id}", response_model=schemas.AlertaResponse)
def update_alerta(
    alerta_id: int,
    alerta: schemas.AlertaUpdate,
    db: Session = Depends(get_db)
):

    return crud.actualizar_alerta(
        db=db,
        alerta_id=alerta_id,
        alerta=alerta
    )