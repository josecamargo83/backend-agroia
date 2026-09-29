from sqlalchemy import Column, Integer, String, Text
from app.core.config import Base


class TipoSuelo(Base):
    __tablename__ = "tipos_suelo"

    TipoSuelo_Id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    TipoSuelo_Nombre = Column(String(100), nullable=False, unique=True)
    TipoSuelo_Descripcion = Column(Text, nullable=True)