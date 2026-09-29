from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.core.config import Base


class Sensor(Base):
    __tablename__ = "sensores"

    Sensor_Id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    Lote_Id = Column(
        Integer,
        ForeignKey("lotes_tierra.Lote_Id"),
        nullable=False
    )

    TipoSensor_Id = Column(
        Integer,
        ForeignKey("tipo_sensor.TipoSensor_Id"),
        nullable=False
    )

    Sensor_Nombre = Column(String(100), nullable=False)
    Sensor_NumeroSerie = Column(String(100), nullable=False, unique=True)
    Sensor_FechaInstalacion = Column(Date, nullable=True)
    Sensor_Estado = Column(String(30), nullable=False, default="ACTIVO")