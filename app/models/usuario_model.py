from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.config import Base

class Usuarios(Base):
    __tablename__ = "usuarios"

    Usuario_Id = Column("Usuario_Id", Integer, primary_key=True, index=True)
    Usuario_Nombres = Column("Usuario_Nombres", String(100), nullable=False)
    Usuario_Mail = Column("Usuario_Mail", String(150), nullable=False, unique=True)
    Usuario_Telefono = Column("Usuario_Telefono", String(20), nullable=True)
    Usuario_Nombre = Column("Usuario_Nombre", String(50), nullable=False, unique=True, index=True)
    Usuario_Password = Column("Usuario_Password", String(255), nullable=False)

    TipoUsuario_Id = Column("TipoUsuario_Id", Integer, ForeignKey("tipo_usuario.TipoUsuario_Id"), nullable=False)
    EstadoUsuario_Id = Column("EstadoUsuario_Id", Integer, ForeignKey("estado_usuario.EstadoUsuario_Id"), nullable=False)