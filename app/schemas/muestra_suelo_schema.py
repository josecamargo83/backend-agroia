from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MuestraSensorResponse(BaseModel):
    Sensor_Id: int
    Sensor_Nombre: str

    class Config:
        from_attributes = True


class MuestraParametroResponse(BaseModel):
    Parametro_Id: int
    Parametro_Nombre: str
    Parametro_Unidad: str

    class Config:
        from_attributes = True


class MuestraSueloBase(BaseModel):
    Sensor_Id: int
    Parametro_Id: int
    Muestra_Valor: float
    Muestra_FechaHora: Optional[datetime] = None


class MuestraSueloCreate(BaseModel):
    Sensor_Id: int
    Parametro_Id: int
    Muestra_Valor: float
    Muestra_FechaHora: Optional[datetime] = None


class MuestraSueloUpdate(BaseModel):
    Sensor_Id: Optional[int] = None
    Parametro_Id: Optional[int] = None
    Muestra_Valor: Optional[float] = None
    Muestra_FechaHora: Optional[datetime] = None


class MuestraSueloResponse(MuestraSueloBase):
    Muestra_Id: int

    class Config:
        from_attributes = True