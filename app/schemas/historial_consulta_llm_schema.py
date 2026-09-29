from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class HistorialUsuarioResponse(BaseModel):
    User_Id: int
    User_Names: str
    User_Name: str

    class Config:
        from_attributes = True


class HistorialConsultaLLMBase(BaseModel):
    User_Id: int
    Historial_Prompt: str
    Historial_Respuesta: Optional[str] = None
    Historial_Modelo: Optional[str] = None
    Historial_FechaHora: Optional[datetime] = None


class HistorialConsultaLLMCreate(BaseModel):
    User_Id: int
    Historial_Prompt: str
    Historial_Respuesta: Optional[str] = None
    Historial_Modelo: Optional[str] = None


class HistorialConsultaLLMResponse(HistorialConsultaLLMBase):
    Historial_Id: int

    class Config:
        from_attributes = True