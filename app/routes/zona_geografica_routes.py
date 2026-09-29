from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth_token import decode_token
from app.core.config import get_db

import app.crud.zona_geografica_crud as crud
import app.schemas.zona_geografica_schema as schemas


app = APIRouter()


@app.get("/list")
def list_zonas(db: Session = Depends(get_db)):
    return crud.get_zonas(db=db)


@app.get("/{zona_id}", response_model=schemas.ZonaGeograficaResponse)
def get_zona(zona_id: int, db: Session = Depends(get_db)):

    zona = crud.get_zona(db=db, zona_id=zona_id)

    if zona is None:
        raise HTTPException(
            status_code=404,
            detail="Zona geográfica no encontrada"
        )

    return zona


@app.post(
    "/create",response_model=schemas.ZonaGeograficaResponse)
def create_zona(
    zona: schemas.ZonaGeograficaCreate,
    db: Session = Depends(get_db)
):
    return crud.crear_zona(db=db, zona=zona)


@app.put(
    "/update/{zona_id}", response_model=schemas.ZonaGeograficaResponse)
def update_zona(
    zona_id: int,
    zona: schemas.ZonaGeograficaUpdate,
    db: Session = Depends(get_db)
):
    return crud.actualizar_zona(
        db=db,
        zona_id=zona_id,
        zona=zona
    )