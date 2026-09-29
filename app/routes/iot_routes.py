from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth_token import decode_token
from app.core.config import get_db

from app.core.influxdb import consultar_influxdb

import app.crud.configuracion_iot_crud as crud
import app.schemas.configuracion_iot_schema as schemas


app = APIRouter()


@app.get(
    "/configuracion",
    response_model=schemas.ConfiguracionIOTResponse
)
def get_configuracion(
    db: Session = Depends(get_db)
):
    return crud.get_configuracion(db=db)


@app.put(
    "/configuracion",
    response_model=schemas.ConfiguracionIOTResponse
)
def update_configuracion(
    configuracion: schemas.ConfiguracionIOTUpdate,
    db: Session = Depends(get_db)
):
    return crud.actualizar_configuracion(
        db=db,
        configuracion=configuracion
    )


# ============================================================
# ÚLTIMA MEDICIÓN IOT
# ============================================================

@app.get("/ultima-medicion")
def ultima_medicion():

    query = """
        SELECT *
        FROM muestras_suelo
        ORDER BY time DESC
        LIMIT 1
    """

    try:

        resultado = consultar_influxdb(query)

        return {
            "fuente": "InfluxDB",
            "medicion": resultado
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Error consultando InfluxDB: {str(e)}"
        )


# ============================================================
# HISTORIAL DE TELEMETRÍA IOT
# ============================================================

@app.get("/historial")
def historial_mediciones():

    query = """
        SELECT *
        FROM muestras_suelo
        ORDER BY time DESC
        LIMIT 500
    """

    try:

        resultado = consultar_influxdb(query)

        return {
            "fuente": "InfluxDB",
            "cantidad": len(resultado),
            "mediciones": resultado
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Error consultando historial en InfluxDB: {str(e)}"
        )
