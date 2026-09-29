from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.tipo_suelo_model import TipoSuelo
from app.schemas.tipo_suelo_schema import (
    TipoSueloCreate,
    TipoSueloUpdate
)


def get_tipos_suelo(db: Session):
    return db.query(TipoSuelo).all()


def get_tipo_suelo(db: Session, tipo_suelo_id: int):
    return db.query(TipoSuelo).filter(
        TipoSuelo.TipoSuelo_Id == tipo_suelo_id
    ).first()


def crear_tipo_suelo(db: Session, tipo_suelo: TipoSueloCreate):

    existente = db.query(TipoSuelo).filter(
        TipoSuelo.TipoSuelo_Nombre == tipo_suelo.TipoSuelo_Nombre
    ).first()

    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El tipo de suelo ya existe"
        )

    db_tipo = TipoSuelo(
        **tipo_suelo.model_dump()
    )

    db.add(db_tipo)
    db.commit()
    db.refresh(db_tipo)

    return db_tipo


def actualizar_tipo_suelo(
    db: Session,
    tipo_suelo_id: int,
    tipo_suelo: TipoSueloUpdate
):

    db_tipo = get_tipo_suelo(db, tipo_suelo_id)

    if not db_tipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de suelo no encontrado"
        )

    datos = tipo_suelo.model_dump(exclude_unset=True)

    for campo, valor in datos.items():
        setattr(db_tipo, campo, valor)

    db.commit()
    db.refresh(db_tipo)

    return db_tipo