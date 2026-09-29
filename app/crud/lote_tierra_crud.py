from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.lote_tierra_model import LoteTierra
from app.schemas.lote_tierra_schema import (
    LoteTierraCreate,
    LoteTierraUpdate
)


def get_lotes(db: Session):
    return db.query(LoteTierra).all()


def get_lote(db: Session, lote_id: int):
    return db.query(LoteTierra).filter(
        LoteTierra.Lote_Id == lote_id
    ).first()


def crear_lote(db: Session, lote: LoteTierraCreate):

    db_lote = LoteTierra(
        **lote.model_dump()
    )

    db.add(db_lote)
    db.commit()
    db.refresh(db_lote)

    return db_lote


def actualizar_lote(
    db: Session,
    lote_id: int,
    lote: LoteTierraUpdate
):

    db_lote = get_lote(db, lote_id)

    if not db_lote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lote no encontrado"
        )

    datos = lote.model_dump(exclude_unset=True)

    for campo, valor in datos.items():
        setattr(db_lote, campo, valor)

    db.commit()
    db.refresh(db_lote)

    return db_lote