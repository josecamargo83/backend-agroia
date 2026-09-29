from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DeteccionVisionCreate(BaseModel):
    Lote_Id: Optional[int] = None
    Deteccion_Archivo: Optional[str] = None
    Deteccion_Clase: str
    Deteccion_Confianza: float
    Deteccion_XMin: Optional[int] = None
    Deteccion_YMin: Optional[int] = None
    Deteccion_XMax: Optional[int] = None
    Deteccion_YMax: Optional[int] = None


class DeteccionVisionResponse(BaseModel):
    Deteccion_Id: int
    Lote_Id: Optional[int] = None
    Deteccion_Archivo: Optional[str] = None
    Deteccion_Clase: str
    Deteccion_Confianza: float
    Deteccion_XMin: Optional[int] = None
    Deteccion_YMin: Optional[int] = None
    Deteccion_XMax: Optional[int] = None
    Deteccion_YMax: Optional[int] = None
    Deteccion_FechaHora: datetime

    class Config:
        from_attributes = True