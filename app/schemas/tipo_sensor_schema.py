from pydantic import BaseModel
from typing import Optional


class TipoSensorBase(BaseModel):
    TipoSensor_Nombre: str
    TipoSensor_Descripcion: Optional[str] = None


class TipoSensorCreate(TipoSensorBase):
    pass


class TipoSensorUpdate(BaseModel):
    TipoSensor_Nombre: Optional[str] = None
    TipoSensor_Descripcion: Optional[str] = None


class TipoSensorResponse(TipoSensorBase):
    TipoSensor_Id: int

    class Config:
        from_attributes = True