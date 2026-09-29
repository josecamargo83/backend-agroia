from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from app.core.config import Base


class Alerta(Base):
    __tablename__ = "alertas"

    Alerta_Id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    Muestra_Id = Column(Integer,ForeignKey("muestras_suelo.Muestra_Id"),nullable=False)

    Alerta_Tipo = Column(String(100), nullable=False)
    Alerta_Mensaje = Column(Text, nullable=False)
    Alerta_Nivel = Column(String(30), nullable=False)

    Alerta_FechaHora = Column(
        DateTime,
        nullable=False
    )

    Alerta_Estado = Column(
        String(30),
        nullable=False,
        default="ACTIVA"
    )