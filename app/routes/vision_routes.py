from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form,
    WebSocket,
    WebSocketDisconnect
)

from fastapi.responses import FileResponse
from app.services.reporte_pdf_service import generar_reporte_pdf

import os
import shutil
import cv2
import numpy as np

from app.core.influxdb import consultar_influxdb

from sqlalchemy.orm import Session

from app.services.yolo_service import (
    analizar_imagen,
    analizar_frame
)

from app.core.auth_token import decode_token
from app.core.config import get_db

import app.crud.deteccion_vision_crud as crud
import app.schemas.deteccion_vision_schema as schemas


app = APIRouter()


@app.get(
    "/list",
    response_model=list[schemas.DeteccionVisionResponse]
)
def list_detecciones(
    db: Session = Depends(get_db)
):
    return crud.get_detecciones(db=db)


@app.get("/camara")
def pagina_stream():

    ruta_html = os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(__file__)
            )
        ),
        "frontend",
        "vision_stream.html"
    )

    return FileResponse(ruta_html)

# ============================================================
# GENERAR REPORTE PDF
# ============================================================

@app.post("/reporte-pdf")
async def generar_reporte(
    archivo: UploadFile = File(...)
):

    extension = os.path.splitext(
        archivo.filename
    )[1].lower()

    extensiones_permitidas = [
        ".jpg",
        ".jpeg",
        ".png"
    ]

    if extension not in extensiones_permitidas:

        raise HTTPException(
            status_code=400,
            detail="Formato de imagen no permitido"
        )

    # ========================================================
    # GUARDAR IMAGEN
    # ========================================================

    carpeta_uploads = os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(__file__)
            )
        ),
        "uploads"
    )

    os.makedirs(
        carpeta_uploads,
        exist_ok=True
    )

    nombre_archivo = archivo.filename

    ruta_imagen = os.path.join(
        carpeta_uploads,
        nombre_archivo
    )

    with open(
        ruta_imagen,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            archivo.file,
            buffer
        )

    # ========================================================
    # YOLO
    # ========================================================

    detecciones = analizar_imagen(
        ruta_imagen
    )

    # ========================================================
    # INFLUXDB
    # ========================================================

    query = """
        SELECT *
        FROM muestras_suelo
        ORDER BY time DESC
        LIMIT 1
    """

    try:

        resultado_influx = consultar_influxdb(
            query
        )

        if resultado_influx:

            telemetria = resultado_influx[0]

        else:

            telemetria = {}

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Error consultando InfluxDB: {str(e)}"
        )

    # ========================================================
    # CONVERTIR DETECCIONES
    # ========================================================

    detecciones_pdf = []

    for deteccion in detecciones:

        detecciones_pdf.append({

            "clase": deteccion["clase"],

            "confianza": deteccion[
                "confianza"
            ],

            "bbox": {

                "x1": deteccion["x_min"],

                "y1": deteccion["y_min"],

                "x2": deteccion["x_max"],

                "y2": deteccion["y_max"]

            }

        })

    # ========================================================
    # GENERAR PDF
    # ========================================================

    nombre_pdf = (
        "reporte_agroia.pdf"
    )

    ruta_pdf = os.path.join(
        carpeta_uploads,
        nombre_pdf
    )

    generar_reporte_pdf(

        ruta_salida=ruta_pdf,

        archivo_imagen=ruta_imagen,

        detecciones=detecciones_pdf,

        telemetria=telemetria

    )

    # ========================================================
    # RESPONDER PDF
    # ========================================================

    return FileResponse(

        path=ruta_pdf,

        media_type="application/pdf",

        filename=nombre_pdf

    )
    

@app.get(
    "/{deteccion_id}",
    response_model=schemas.DeteccionVisionResponse
)
def get_deteccion(
    deteccion_id: int,
    db: Session = Depends(get_db)
):

    deteccion = crud.get_deteccion(
        db=db,
        deteccion_id=deteccion_id
    )

    if deteccion is None:
        raise HTTPException(
            status_code=404,
            detail="Detección no encontrada"
        )

    return deteccion


@app.post(
    "/create",
    response_model=schemas.DeteccionVisionResponse
)
def create_deteccion(
    deteccion: schemas.DeteccionVisionCreate,
    db: Session = Depends(get_db)
):

    return crud.crear_deteccion(
        db=db,
        deteccion=deteccion
    )


@app.post(
    "/analizar"
)
def analizar_vision(
    archivo: UploadFile = File(...),
    lote_id: int | None = Form(None),
    db: Session = Depends(get_db)
):

    # ========================================================
    # VALIDAR EXTENSIÓN
    # ========================================================

    extensiones_permitidas = [
        ".jpg",
        ".jpeg",
        ".png"
    ]

    extension = os.path.splitext(
        archivo.filename
    )[1].lower()

    if extension not in extensiones_permitidas:
        raise HTTPException(
            status_code=400,
            detail="Solo se permiten imágenes JPG, JPEG o PNG"
        )

    # ========================================================
    # CREAR CARPETA DE IMÁGENES
    # ========================================================

    carpeta = "uploads/vision"

    os.makedirs(
        carpeta,
        exist_ok=True
    )

    # ========================================================
    # GUARDAR IMAGEN
    # ========================================================

    archivo_path = os.path.join(
        carpeta,
        archivo.filename
    )

    with open(archivo_path, "wb") as buffer:

        shutil.copyfileobj(
            archivo.file,
            buffer
        )

    # ========================================================
    # EJECUTAR YOLO
    # ========================================================

    detecciones = analizar_imagen(
        archivo_path
    )

    # ========================================================
    # GUARDAR DETECCIONES EN BASE DE DATOS
    # ========================================================

    detecciones_guardadas = []

    for deteccion in detecciones:

        nueva_deteccion = schemas.DeteccionVisionCreate(
            Lote_Id=lote_id,
            Deteccion_Archivo=archivo.filename,
            Deteccion_Clase=deteccion["clase"],
            Deteccion_Confianza=deteccion["confianza"],
            Deteccion_XMin=deteccion["x_min"],
            Deteccion_YMin=deteccion["y_min"],
            Deteccion_XMax=deteccion["x_max"],
            Deteccion_YMax=deteccion["y_max"]
        )

        deteccion_guardada = crud.crear_deteccion(
            db=db,
            deteccion=nueva_deteccion
        )

        detecciones_guardadas.append(
            deteccion_guardada
        )

    # ========================================================
    # RESPUESTA
    # ========================================================

    return {
        "archivo": archivo.filename,
        "cantidad_detecciones": len(detecciones_guardadas),
        "detecciones": [
            {
                "id": deteccion.Deteccion_Id,
                "clase": deteccion.Deteccion_Clase,
                "confianza": float(
                    deteccion.Deteccion_Confianza
                ),
                "x_min": deteccion.Deteccion_XMin,
                "y_min": deteccion.Deteccion_YMin,
                "x_max": deteccion.Deteccion_XMax,
                "y_max": deteccion.Deteccion_YMax
            }
            for deteccion in detecciones_guardadas
        ]
    }




# ============================================================
# FUSIÓN: TELEMETRÍA IOT + DETECCIONES YOLO
# ============================================================

@app.post("/fusion")
def fusionar_iot_y_vision(
    archivo: UploadFile = File(...),
):
    extensiones_permitidas = [
        ".jpg",
        ".jpeg",
        ".png"
    ]

    extension = os.path.splitext(
        archivo.filename
    )[1].lower()

    if extension not in extensiones_permitidas:
        raise HTTPException(
            status_code=400,
            detail="Solo se permiten imágenes JPG, JPEG o PNG"
        )

    # --------------------------------------------------------
    # 1. GUARDAR IMAGEN
    # --------------------------------------------------------

    carpeta = "uploads/vision"

    os.makedirs(
        carpeta,
        exist_ok=True
    )

    archivo_path = os.path.join(
        carpeta,
        archivo.filename
    )

    with open(archivo_path, "wb") as buffer:
        shutil.copyfileobj(
            archivo.file,
            buffer
        )

    # --------------------------------------------------------
    # 2. ANALIZAR IMAGEN CON YOLO
    # --------------------------------------------------------

    try:
        detecciones = analizar_imagen(
            archivo_path
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analizando imagen con YOLO: {str(e)}"
        )

    # --------------------------------------------------------
    # 3. CONSULTAR ÚLTIMA TELEMETRÍA EN INFLUXDB
    # --------------------------------------------------------

    query = """
        SELECT *
        FROM muestras_suelo
        ORDER BY time DESC
        LIMIT 1
    """

    try:
        resultado = consultar_influxdb(query)

    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Error consultando InfluxDB: {str(e)}"
        )

    if not resultado:
        raise HTTPException(
            status_code=404,
            detail="No hay mediciones disponibles en InfluxDB"
        )

    medicion = resultado[0]

    # --------------------------------------------------------
    # 4. CONSTRUIR RESPUESTA FUSIONADA
    # --------------------------------------------------------

    return {
        "archivo": archivo.filename,

        "telemetria": {
            "humedad_suelo": medicion.get("humedad_suelo"),
            "temp_aire": medicion.get("temp_aire"),
            "humedad_aire": medicion.get("humedad_aire"),
            "ph": medicion.get("ph"),
            "tds": medicion.get("tds"),
            "fecha_medicion": medicion.get("time"),
            "topic": medicion.get("topic")
        },

        "cantidad_detecciones": len(detecciones),

        "detecciones": [
            {
                "clase": deteccion["clase"],
                "confianza": deteccion["confianza"],
                "bbox": {
                    "x1": deteccion["x_min"],
                    "y1": deteccion["y_min"],
                    "x2": deteccion["x_max"],
                    "y2": deteccion["y_max"]
                }
            }
            for deteccion in detecciones
        ]
    }



# ============================================================
# STREAM DE CÁMARA EN TIEMPO REAL
# ============================================================

# ============================================================
# STREAM DE CÁMARA EN TIEMPO REAL
# ============================================================

@app.websocket("/stream")
async def vision_stream(websocket: WebSocket):

    await websocket.accept()

    try:

        while True:

            datos = await websocket.receive_bytes()

            array = np.frombuffer(
                datos,
                dtype=np.uint8
            )

            frame = cv2.imdecode(
                array,
                cv2.IMREAD_COLOR
            )

            if frame is None:

                await websocket.send_json({
                    "error": "No se pudo procesar el frame"
                })

                continue

            # ====================================================
            # YOLO
            # ====================================================

            detecciones = analizar_frame(frame)

            # ====================================================
            # INFLUXDB
            # ====================================================

            query = """
                SELECT *
                FROM muestras_suelo
                ORDER BY time DESC
                LIMIT 1
            """

            try:

                resultado_influx = consultar_influxdb(query)

                if resultado_influx:

                    telemetria = resultado_influx[0]

                else:

                    telemetria = None

            except Exception as e:

                telemetria = {
                    "error": str(e)
                }

            # ====================================================
            # RESPUESTA
            # ====================================================

            respuesta = {

                "cantidad_detecciones": len(
                    detecciones
                ),

                "detecciones": [],

                "telemetria": telemetria
            }

            for deteccion in detecciones:

                respuesta["detecciones"].append({

                    "clase": deteccion["clase"],

                    "confianza": deteccion[
                        "confianza"
                    ],

                    "bbox": {

                        "x1": deteccion[
                            "x_min"
                        ],

                        "y1": deteccion[
                            "y_min"
                        ],

                        "x2": deteccion[
                            "x_max"
                        ],

                        "y2": deteccion[
                            "y_max"
                        ]

                    }

                })

            await websocket.send_json(
                respuesta
            )

    except WebSocketDisconnect:

        print(
            "Cliente desconectado del stream de visión"
        )

