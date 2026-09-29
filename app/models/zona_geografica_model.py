from sqlalchemy import Column, Integer, String, Text, Numeric
from app.core.config import Base


class ZonaGeografica(Base):
    __tablename__ = "zonas_geograficas"

    Zona_Id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Zona_Nombre = Column(String(150), nullable=False)
    Zona_Descripcion = Column(Text, nullable=True)
    Zona_Departamento = Column(String(100), nullable=True)
    Zona_Municipio = Column(String(100), nullable=True)
    Zona_Latitud = Column(Numeric(10, 7), nullable=True)
    Zona_Longitud = Column(Numeric(10, 7), nullable=True)