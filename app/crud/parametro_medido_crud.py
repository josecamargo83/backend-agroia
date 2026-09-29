from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.parametro_medido_model import ParametroMedido
from app.schemas.parametro_medido_schema import (
    ParametroMedidoCreate,
    ParametroMedidoUpdate
)


def get_parametros(db: Session):
    return db.query(ParametroMedido).all()


def get_parametro(db: Session, parametro_id: int):
    return db.query(ParametroMedido).filter(
        ParametroMedido.Parametro_Id == parametro_id
    ).first()


def crear_parametro(
    db: Session,
    parametro: ParametroMedidoCreate
):

    existente = db.query(ParametroMedido).filter(
        ParametroMedido.Parametro_Nombre ==
        parametro.Parametro_Nombre
    ).first()

    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El parámetro ya existe"
        )

    db_parametro = ParametroMedido(
        **parametro.model_dump()
    )

    db.add(db_parametro)
    db.commit()
    db.refresh(db_parametro)

    return db_parametro


def actualizar_parametro(
    db: Session,
    parametro_id: int,
    parametro: ParametroMedidoUpdate
):

    db_parametro = get_parametro(db, parametro_id)

    if not db_parametro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parámetro no encontrado"
        )

    datos = parametro.model_dump(exclude_unset=True)

    for campo, valor in datos.items():
        setattr(db_parametro, campo, valor)

    db.commit()
    db.refresh(db_parametro)

    return db_parametro