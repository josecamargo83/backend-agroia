from pydantic import BaseModel


class ConfiguracionIOTUpdate(BaseModel):
    Intervalo_EnvioSegundos: int


class ConfiguracionIOTResponse(BaseModel):
    Configuracion_Id: int
    Intervalo_EnvioSegundos: int
    Configuracion_FechaActualizacion: object

    class Config:
        from_attributes = True