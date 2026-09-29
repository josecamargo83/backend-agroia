from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth_token import decode_token
from app.core.config import get_db

import app.crud.tipo_suelo_crud as crud
import app.schemas.tipo_suelo_schema as schemas


app = APIRouter()


@app.get("/list")
def list_tipos_suelo(db: Session = Depends(get_db)):
    return crud.get_tipos_suelo(db=db)


@app.get(
    "/{tipo_suelo_id}",
    
    response_model=schemas.TipoSueloResponse
)
def get_tipo_suelo(
    tipo_suelo_id: int,
    db: Session = Depends(get_db)
):

    tipo = crud.get_tipo_suelo(
        db=db,
        tipo_suelo_id=tipo_suelo_id
    )

    if tipo is None:
        raise HTTPException(
            status_code=404,
            detail="Tipo de suelo no encontrado"
        )

    return tipo


@app.post(
    "/create",
    
    response_model=schemas.TipoSueloResponse
)
def create_tipo_suelo(
    tipo_suelo: schemas.TipoSueloCreate,
    db: Session = Depends(get_db)
):
    return crud.crear_tipo_suelo(
        db=db,
        tipo_suelo=tipo_suelo
    )


@app.put(
    "/update/{tipo_suelo_id}",
    
    response_model=schemas.TipoSueloResponse
)
def update_tipo_suelo(
    tipo_suelo_id: int,
    tipo_suelo: schemas.TipoSueloUpdate,
    db: Session = Depends(get_db)
):
    return crud.actualizar_tipo_suelo(
        db=db,
        tipo_suelo_id=tipo_suelo_id,
        tipo_suelo=tipo_suelo
    )