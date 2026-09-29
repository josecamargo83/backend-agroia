from pydantic import BaseModel
from typing import Optional


class TipoSueloBase(BaseModel):
    TipoSuelo_Nombre: str
    TipoSuelo_Descripcion: Optional[str] = None


class TipoSueloCreate(TipoSueloBase):
    pass


class TipoSueloUpdate(BaseModel):
    TipoSuelo_Nombre: Optional[str] = None
    TipoSuelo_Descripcion: Optional[str] = None


class TipoSueloResponse(TipoSueloBase):
    TipoSuelo_Id: int

    class Config:
        from_attributes = True