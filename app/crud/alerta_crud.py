from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.alerta_model import Alerta
from app.models.muestra_suelo_model import MuestraSuelo

from app.schemas.alerta_schema import (
    AlertaCreate,
    AlertaUpdate
)


def get_alertas(db: Session):
    return db.query(Alerta).order_by(
        Alerta.Alerta_FechaHora.desc()
    ).all()


def get_alerta(db: Session, alerta_id: int):
    return db.query(Alerta).filter(
        Alerta.Alerta_Id == alerta_id
    ).first()


def crear_alerta(db: Session, alerta: AlertaCreate):

    muestra = db.query(MuestraSuelo).filter(
        MuestraSuelo.Muestra_Id == alerta.Muestra_Id
    ).first()

    if not muestra:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Muestra no encontrada"
        )

    datos = alerta.model_dump()

    if datos.get("Alerta_FechaHora") is None:
        from datetime import datetime
        datos["Alerta_FechaHora"] = datetime.now()

    db_alerta = Alerta(**datos)

    db.add(db_alerta)
    db.commit()
    db.refresh(db_alerta)

    return db_alerta


def actualizar_alerta(
    db: Session,
    alerta_id: int,
    alerta: AlertaUpdate
):

    db_alerta = get_alerta(db, alerta_id)

    if not db_alerta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alerta no encontrada"
        )

    datos = alerta.model_dump(exclude_unset=True)

    for campo, valor in datos.items():
        setattr(db_alerta, campo, valor)

    db.commit()
    db.refresh(db_alerta)

    return db_alerta