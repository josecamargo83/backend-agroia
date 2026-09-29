from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime

from app.models.deteccion_vision_model import DeteccionVision
from app.models.lote_tierra_model import LoteTierra

from app.schemas.deteccion_vision_schema import (
    DeteccionVisionCreate
)


def get_detecciones(db: Session):
    return db.query(DeteccionVision).all()


def get_deteccion(
    db: Session,
    deteccion_id: int
):
    return db.query(DeteccionVision).filter(
        DeteccionVision.Deteccion_Id == deteccion_id
    ).first()


def crear_deteccion(
    db: Session,
    deteccion: DeteccionVisionCreate
):

    if deteccion.Lote_Id is not None:

        lote = db.query(LoteTierra).filter(
            LoteTierra.Lote_Id == deteccion.Lote_Id
        ).first()

        if not lote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lote no encontrado"
            )

    db_deteccion = DeteccionVision(
        Lote_Id=deteccion.Lote_Id,
        Deteccion_Archivo=deteccion.Deteccion_Archivo,
        Deteccion_Clase=deteccion.Deteccion_Clase,
        Deteccion_Confianza=deteccion.Deteccion_Confianza,
        Deteccion_XMin=deteccion.Deteccion_XMin,
        Deteccion_YMin=deteccion.Deteccion_YMin,
        Deteccion_XMax=deteccion.Deteccion_XMax,
        Deteccion_YMax=deteccion.Deteccion_YMax,
        Deteccion_FechaHora=datetime.now()
    )

    db.add(db_deteccion)
    db.commit()
    db.refresh(db_deteccion)

    return db_deteccion