from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from app.core.config import Base


class DeteccionVision(Base):
    __tablename__ = "detecciones_vision"

    Deteccion_Id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    Lote_Id = Column(
        Integer,
        ForeignKey("lotes_tierra.Lote_Id"),
        nullable=True
    )

    Deteccion_Archivo = Column(
        String(255),
        nullable=True
    )

    Deteccion_Clase = Column(
        String(100),
        nullable=False
    )

    Deteccion_Confianza = Column(
        Numeric(6, 2),
        nullable=False
    )

    Deteccion_XMin = Column(
        Integer,
        nullable=True
    )

    Deteccion_YMin = Column(
        Integer,
        nullable=True
    )

    Deteccion_XMax = Column(
        Integer,
        nullable=True
    )

    Deteccion_YMax = Column(
        Integer,
        nullable=True
    )

    Deteccion_FechaHora = Column(
        DateTime,
        nullable=False
    )