from pydantic import BaseModel
from typing import Optional


class ZonaLoteResponse(BaseModel):
    Zona_Id: int
    Zona_Nombre: str

    class Config:
        from_attributes = True


class TipoSueloLoteResponse(BaseModel):
    TipoSuelo_Id: int
    TipoSuelo_Nombre: str

    class Config:
        from_attributes = True


class LoteTierraBase(BaseModel):
    Zona_Id: int
    TipoSuelo_Id: int
    Lote_Nombre: str
    Lote_Descripcion: Optional[str] = None
    Lote_Area: Optional[float] = None


class LoteTierraCreate(LoteTierraBase):
    pass


class LoteTierraUpdate(BaseModel):
    Zona_Id: Optional[int] = None
    TipoSuelo_Id: Optional[int] = None
    Lote_Nombre: Optional[str] = None
    Lote_Descripcion: Optional[str] = None
    Lote_Area: Optional[float] = None


class LoteTierraResponse(LoteTierraBase):
    Lote_Id: int

    class Config:
        from_attributes = True