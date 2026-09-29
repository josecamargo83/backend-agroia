from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from app.core.config import Base


class HistorialConsultaLLM(Base):
    __tablename__ = "historial_consultas_llm"

    Historial_Id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    User_Id = Column(
        Integer,
        ForeignKey('"user".User_Id'),
        nullable=False
    )

    Historial_Prompt = Column(Text, nullable=False)
    Historial_Respuesta = Column(Text, nullable=True)
    Historial_Modelo = Column(String(100), nullable=True)

    Historial_FechaHora = Column(
        DateTime,
        nullable=False
    )