from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AlertaMuestraResponse(BaseModel):
    Muestra_Id: int
    Muestra_Valor: float

    class Config:
        from_attributes = True


class AlertaBase(BaseModel):
    Muestra_Id: int
    Alerta_Tipo: str
    Alerta_Mensaje: str
    Alerta_Nivel: str
    Alerta_FechaHora: Optional[datetime] = None
    Alerta_Estado: str = "ACTIVA"


class AlertaCreate(AlertaBase):
    pass


class AlertaUpdate(BaseModel):
    Muestra_Id: Optional[int] = None
    Alerta_Tipo: Optional[str] = None
    Alerta_Mensaje: Optional[str] = None
    Alerta_Nivel: Optional[str] = None
    Alerta_Estado: Optional[str] = None


class AlertaResponse(AlertaBase):
    Alerta_Id: int

    class Config:
        from_attributes = True