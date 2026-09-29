from pydantic import BaseModel
from typing import Optional
from datetime import date


class SensorLoteResponse(BaseModel):
    Lote_Id: int
    Lote_Nombre: str

    class Config:
        from_attributes = True


class SensorTipoResponse(BaseModel):
    TipoSensor_Id: int
    TipoSensor_Nombre: str

    class Config:
        from_attributes = True


class SensorBase(BaseModel):
    Lote_Id: int
    TipoSensor_Id: int
    Sensor_Nombre: str
    Sensor_NumeroSerie: str
    Sensor_FechaInstalacion: Optional[date] = None
    Sensor_Estado: str = "ACTIVO"


class SensorCreate(SensorBase):
    pass


class SensorUpdate(BaseModel):
    Lote_Id: Optional[int] = None
    TipoSensor_Id: Optional[int] = None
    Sensor_Nombre: Optional[str] = None
    Sensor_NumeroSerie: Optional[str] = None
    Sensor_FechaInstalacion: Optional[date] = None
    Sensor_Estado: Optional[str] = None


class SensorResponse(SensorBase):
    Sensor_Id: int

    class Config:
        from_attributes = True