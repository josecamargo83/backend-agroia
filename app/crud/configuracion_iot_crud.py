from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.configuracion_iot_model import ConfiguracionIOT
from app.schemas.configuracion_iot_schema import ConfiguracionIOTUpdate


def get_configuracion(db: Session):

    configuracion = db.query(ConfiguracionIOT).first()

    if not configuracion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuración IoT no encontrada"
        )

    return configuracion


def actualizar_configuracion(
    db: Session,
    configuracion: ConfiguracionIOTUpdate
):

    if configuracion.Intervalo_EnvioSegundos not in [5, 10, 30]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El intervalo debe ser 5, 10 o 30 segundos"
        )

    db_configuracion = get_configuracion(db)

    db_configuracion.Intervalo_EnvioSegundos = (
        configuracion.Intervalo_EnvioSegundos
    )

    db.commit()
    db.refresh(db_configuracion)

    return db_configuracion