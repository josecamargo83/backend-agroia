from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey
from app.core.config import Base


class MuestraSuelo(Base):
    __tablename__ = "muestras_suelo"

    Muestra_Id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    Sensor_Id = Column(
        Integer,
        ForeignKey("sensores.Sensor_Id"),
        nullable=False
    )

    Parametro_Id = Column(
        Integer,
        ForeignKey("parametros_medidos.Parametro_Id"),
        nullable=False
    )

    Muestra_Valor = Column(Numeric(12, 4), nullable=False)

    Muestra_FechaHora = Column(
        DateTime,
        nullable=False
    )