from sqlalchemy import Column, Integer, String
from app.core.config import Base

class TipoUsuario(Base):
    __tablename__ = "tipo_usuario"

    TipoUsuario_Id = Column("TipoUsuario_Id", Integer, primary_key=True, index=True, autoincrement=True)
    TipoUsuario_Descripcion = Column("TipoUsuario_Descripcion", String(25), nullable=False)