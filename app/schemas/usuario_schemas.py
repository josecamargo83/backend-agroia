from pydantic import BaseModel
from typing import Optional


class TipoUsuarioBase(BaseModel):
    TipoUsuario_Id: int
    TipoUsuario_Descripcion: str

    class Config:
        orm_mode = True


class EstadoUsuarioBase(BaseModel):
    EstadoUsuario_Id: int
    EstadoUsuario_Descripcion: str

    class Config:
        orm_mode = True


class UsuarioBase(BaseModel):
    Usuario_Id: int
    Usuario_Nombres: str
    Usuario_Mail: str
    Usuario_Telefono: Optional[str] = None
    Usuario_Nombre: str
    Usuario_Password: str
    TipoUsuario_Id: Optional[int] = None
    EstadoUsuario_Id: Optional[int] = None

    tipo: Optional[TipoUsuarioBase] = None
    estado: Optional[EstadoUsuarioBase] = None

    class Config:
        orm_mode = True


class UsuarioCreate(BaseModel):
    Usuario_Id: int
    Usuario_Nombres: str
    Usuario_Mail: str
    Usuario_Telefono: Optional[str] = None
    Usuario_Nombre: str
    Usuario_Password: str
    TipoUsuario_Id: Optional[int] = None
    EstadoUsuario_Id: Optional[int] = None


class UsuarioUpdate(BaseModel):
    Usuario_Id: int
    Usuario_Nombres: Optional[str] = None
    Usuario_Mail: Optional[str] = None
    Usuario_Telefono: Optional[str] = None
    Usuario_Nombre: Optional[str] = None
    Usuario_Password: Optional[str] = None
    TipoUsuario_Id: Optional[int] = None
    EstadoUsuario_Id: Optional[int] = None