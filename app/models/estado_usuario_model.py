from sqlalchemy import Column, Integer, String
from app.core.config import Base

class EstadoUsuario(Base):
    __tablename__ = "estado_usuario"

    EstadoUsuario_Id = Column("EstadoUsuario_Id", Integer, primary_key=True, index=True, autoincrement=True)
    EstadoUsuario_Descripcion = Column("EstadoUsuario_Descripcion", String(25), nullable=False)