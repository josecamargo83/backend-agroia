from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth_token import decode_token
from app.core.config import get_db

import app.crud.lote_tierra_crud as crud
import app.schemas.lote_tierra_schema as schemas


app = APIRouter()


@app.get("/list")
def list_lotes(db: Session = Depends(get_db)):
    return crud.get_lotes(db=db)


@app.get(
    "/{lote_id}", response_model=schemas.LoteTierraResponse)
def get_lote(
    lote_id: int,
    db: Session = Depends(get_db)
):

    lote = crud.get_lote(
        db=db,
        lote_id=lote_id
    )

    if lote is None:
        raise HTTPException(
            status_code=404,
            detail="Lote no encontrado"
        )

    return lote


@app.post(
    "/create", response_model=schemas.LoteTierraResponse)
def create_lote(
    lote: schemas.LoteTierraCreate,
    db: Session = Depends(get_db)
):
    return crud.crear_lote(
        db=db,
        lote=lote
    )


@app.put(
    "/update/{lote_id}", response_model=schemas.LoteTierraResponse)
def update_lote(
    lote_id: int,
    lote: schemas.LoteTierraUpdate,
    db: Session = Depends(get_db)
):
    return crud.actualizar_lote(
        db=db,
        lote_id=lote_id,
        lote=lote
    )