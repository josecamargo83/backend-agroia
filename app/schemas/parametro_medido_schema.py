from pydantic import BaseModel
from typing import Optional


class ParametroMedidoBase(BaseModel):
    Parametro_Nombre: str
    Parametro_Unidad: str
    Parametro_Descripcion: Optional[str] = None
    Parametro_ValorMinimo: Optional[float] = None
    Parametro_ValorMaximo: Optional[float] = None


class ParametroMedidoCreate(ParametroMedidoBase):
    pass


class ParametroMedidoUpdate(BaseModel):
    Parametro_Nombre: Optional[str] = None
    Parametro_Unidad: Optional[str] = None
    Parametro_Descripcion: Optional[str] = None
    Parametro_ValorMinimo: Optional[float] = None
    Parametro_ValorMaximo: Optional[float] = None


class ParametroMedidoResponse(ParametroMedidoBase):
    Parametro_Id: int

    class Config:
        from_attributes = True