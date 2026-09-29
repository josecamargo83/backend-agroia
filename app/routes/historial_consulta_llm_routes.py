from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth_token import decode_token
from app.core.config import get_db

import app.crud.historial_consulta_llm_crud as crud
import app.schemas.historial_consulta_llm_schema as schemas


app = APIRouter()


@app.get(
    "/list",
    dependencies=[Depends(decode_token)]
)
def list_consultas_llm(
    db: Session = Depends(get_db)
):

    return crud.get_historial_consultas(db=db)


@app.get(
    "/{historial_id}",
    dependencies=[Depends(decode_token)],
    response_model=schemas.HistorialConsultaLLMResponse
)
def get_consulta_llm(
    historial_id: int,
    db: Session = Depends(get_db)
):

    consulta = crud.get_historial_consulta(
        db=db,
        historial_id=historial_id
    )

    if consulta is None:
        raise HTTPException(
            status_code=404,
            detail="Consulta LLM no encontrada"
        )

    return consulta


@app.post(
    "/create",
    dependencies=[Depends(decode_token)],
    response_model=schemas.HistorialConsultaLLMResponse
)
def create_consulta_llm(
    consulta: schemas.HistorialConsultaLLMCreate,
    db: Session = Depends(get_db)
):

    return crud.crear_consulta_llm(
        db=db,
        consulta=consulta
    )