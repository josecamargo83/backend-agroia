from pydantic import BaseModel
from typing import Optional


class ZonaGeograficaBase(BaseModel):
    Zona_Nombre: str
    Zona_Descripcion: Optional[str] = None
    Zona_Departamento: Optional[str] = None
    Zona_Municipio: Optional[str] = None
    Zona_Latitud: Optional[float] = None
    Zona_Longitud: Optional[float] = None


class ZonaGeograficaCreate(ZonaGeograficaBase):
    pass


class ZonaGeograficaUpdate(BaseModel):
    Zona_Nombre: Optional[str] = None
    Zona_Descripcion: Optional[str] = None
    Zona_Departamento: Optional[str] = None
    Zona_Municipio: Optional[str] = None
    Zona_Latitud: Optional[float] = None
    Zona_Longitud: Optional[float] = None


class ZonaGeograficaResponse(ZonaGeograficaBase):
    Zona_Id: int

    class Config:
        from_attributes = True