from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.zona_geografica_model import ZonaGeografica
from app.schemas.zona_geografica_schema import (
    ZonaGeograficaCreate,
    ZonaGeograficaUpdate
)


def get_zonas(db: Session):
    return db.query(ZonaGeografica).all()


def get_zona(db: Session, zona_id: int):
    return db.query(ZonaGeografica).filter(
        ZonaGeografica.Zona_Id == zona_id
    ).first()


def crear_zona(db: Session, zona: ZonaGeograficaCreate):

    db_zona = ZonaGeografica(
        **zona.model_dump()
    )

    db.add(db_zona)
    db.commit()
    db.refresh(db_zona)

    return db_zona


def actualizar_zona(
    db: Session,
    zona_id: int,
    zona: ZonaGeograficaUpdate
):

    db_zona = get_zona(db, zona_id)

    if not db_zona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Zona geográfica no encontrada"
        )

    datos = zona.model_dump(exclude_unset=True)

    for campo, valor in datos.items():
        setattr(db_zona, campo, valor)

    db.commit()
    db.refresh(db_zona)

    return db_zona