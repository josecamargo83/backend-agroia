from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os

load_dotenv()

# ============================================================
# BASE DE DATOS NEON / POSTGRESQL
# ============================================================

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# ============================================================
# INFLUXDB 3
# ============================================================

INFLUXDB_URL = os.getenv(
    "INFLUXDB_URL",
    "http://localhost:8181"
)

INFLUXDB_DATABASE = os.getenv(
    "INFLUXDB_DATABASE",
    "agroia_suelos"
)

INFLUXDB_TOKEN = os.getenv(
    "INFLUXDB_TOKEN"
)


# ============================================================
# CONEXIÓN A LA BASE DE DATOS
# ============================================================

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()