from fastapi import FastAPI
import uvicorn

from app.core.config import SessionLocal, engine

from app.routes.auth_routes import app as auth_app
from app.routes.usuario_routes import app as user_app

from app.routes.zona_geografica_routes import app as zona_geografica_app
from app.routes.tipo_suelo_routes import app as tipo_suelo_app
from app.routes.lote_tierra_routes import app as lote_tierra_app
from app.routes.tipo_sensor_routes import app as tipo_sensor_app
from app.routes.sensor_routes import app as sensor_app
from app.routes.parametro_medido_routes import app as parametro_medido_app
from app.routes.muestra_suelo_routes import app as muestra_suelo_app
from app.routes.alerta_routes import app as alerta_app
from app.routes.historial_consulta_llm_routes import app as historial_consulta_llm_app

from app.routes.iot_routes import app as iot_app
from app.routes.vision_routes import app as vision_app

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


# ============================================================
# CORS
# ============================================================

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# AUTENTICACIÓN
# ============================================================

app.include_router(auth_app, tags=["Auth"], prefix="/auth")



app.include_router(user_app, tags=["Users"],prefix="/users")
app.include_router(zona_geografica_app, tags=["Zonas Geográficas"], prefix="/zonas_geograficas")
app.include_router(tipo_suelo_app, tags=["Tipos de Suelo"], prefix="/tipos_suelo")
app.include_router(lote_tierra_app, tags=["Lotes de Tierra"], prefix="/lotes")
app.include_router(tipo_sensor_app, tags=["Tipos de Sensor"], prefix="/tipos_sensor")
app.include_router(sensor_app, tags=["Sensores"], prefix="/sensores")
app.include_router(parametro_medido_app, tags=["Parámetros Medidos"], prefix="/parametros")
app.include_router(muestra_suelo_app, tags=["Muestras de Suelo"], prefix="/muestras")
app.include_router(alerta_app, tags=["Alertas"], prefix="/alertas")
app.include_router(historial_consulta_llm_app, tags=["Historial LLM"], prefix="/consultas-llm")

app.include_router(
    iot_app,
    tags=["IoT"],
    prefix="/iot"
)

app.include_router(
    vision_app,
    tags=["Visión"],
    prefix="/vision"
)


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)