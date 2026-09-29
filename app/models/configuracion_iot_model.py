from sqlalchemy import Column, Integer, DateTime
from app.core.config import Base


class ConfiguracionIOT(Base):
    __tablename__ = "configuracion_iot"

    Configuracion_Id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    Intervalo_EnvioSegundos = Column(
        Integer,
        nullable=False,
        default=10
    )

    Configuracion_FechaActualizacion = Column(
        DateTime,
        nullable=False
    )