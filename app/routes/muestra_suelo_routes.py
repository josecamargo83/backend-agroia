from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth_token import decode_token
from app.core.config import get_db

import app.crud.muestra_suelo_crud as crud
import app.schemas.muestra_suelo_schema as schemas


app = APIRouter()


# ============================================================
# GET /api/muestras
# Consultar muestras
# ============================================================

@app.get("/list")
def list_muestras(db: Session = Depends(get_db)):

    return crud.get_muestras(db=db)


# ============================================================
# GET /api/muestras/{muestra_id}
# ============================================================

@app.get(
    "/{muestra_id}", response_model=schemas.MuestraSueloResponse)
def get_muestra(
    muestra_id: int,
    db: Session = Depends(get_db)
):

    muestra = crud.get_muestra(
        db=db,
        muestra_id=muestra_id
    )

    if muestra is None:
        raise HTTPException(
            status_code=404,
            detail="Muestra no encontrada"
        )

    return muestra


# ============================================================
# POST /api/muestras
# Recibir datos del ESP32
# ============================================================

@app.post(
    "/create",
    response_model=schemas.MuestraSueloResponse
)
def create_muestra(
    muestra: schemas.MuestraSueloCreate,
    db: Session = Depends(get_db)
):

    return crud.crear_muestra(
        db=db,
        muestra=muestra
    )