from sqlalchemy import Column, Integer, String, Text, Numeric
from app.core.config import Base


class ParametroMedido(Base):
    __tablename__ = "parametros_medidos"

    Parametro_Id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Parametro_Nombre = Column(String(100), nullable=False, unique=True)
    Parametro_Unidad = Column(String(30), nullable=False)
    Parametro_Descripcion = Column(Text, nullable=True)
    Parametro_ValorMinimo = Column(Numeric(12, 4), nullable=True)
    Parametro_ValorMaximo = Column(Numeric(12, 4), nullable=True)