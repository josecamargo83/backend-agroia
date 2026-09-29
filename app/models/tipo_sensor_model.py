from sqlalchemy import Column, Integer, String, Text
from app.core.config import Base


class TipoSensor(Base):
    __tablename__ = "tipo_sensor"

    TipoSensor_Id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    TipoSensor_Nombre = Column(String(100), nullable=False, unique=True)
    TipoSensor_Descripcion = Column(Text, nullable=True)