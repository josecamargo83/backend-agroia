from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.historial_consulta_llm_model import HistorialConsultaLLM
from app.models.usuario_model import Usuarios

from app.schemas.historial_consulta_llm_schema import (
    HistorialConsultaLLMCreate
)


def get_historial_consultas(db: Session):
    return db.query(
        HistorialConsultaLLM
    ).order_by(
        HistorialConsultaLLM.Historial_FechaHora.desc()
    ).all()


def get_historial_consulta(
    db: Session,
    historial_id: int
):

    return db.query(
        HistorialConsultaLLM
    ).filter(
        HistorialConsultaLLM.Historial_Id == historial_id
    ).first()


def crear_consulta_llm(
    db: Session,
    consulta: HistorialConsultaLLMCreate
):

    usuario = db.query(Usuarios).filter(
        Usuarios.User_Id == consulta.User_Id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    from datetime import datetime

    db_consulta = HistorialConsultaLLM(
        User_Id=consulta.User_Id,
        Historial_Prompt=consulta.Historial_Prompt,
        Historial_Respuesta=consulta.Historial_Respuesta,
        Historial_Modelo=consulta.Historial_Modelo,
        Historial_FechaHora=(
            consulta.Historial_FechaHora
            or datetime.now()
        )
    )

    db.add(db_consulta)
    db.commit()
    db.refresh(db_consulta)

    return db_consulta