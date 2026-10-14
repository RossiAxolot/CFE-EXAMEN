from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ClienteRespuesta(BaseModel):
    id_cliente: int
    nombre_cliente: str
    direccion: str
    active: bool


class ClienteCrear(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nombre_cliente: str = Field(
        min_length=15,
        max_length=100,
        description="Ingrese el nombre completo del cliente",
        examples=["Rosa Isela Rodriguez"],
    )
    direccion: str = Field(
        min_length=25,
        max_length=200,
        description="Ingrese la dirección del domicilio del cliente",
        examples=["Morones Prieto 224, San Pedro Garza Garcia, N.L"],
    )


class ClienteActualizar(BaseModel):
    """Datos requeridos para reemplazar el nombre y la direccion de un cliente."""

    model_config = ConfigDict(str_strip_whitespace=True)

    nombre_cliente: str = Field(
        min_length=15,
        max_length=100,
        description="Ingrese el nuevo nombre completo del cliente",
        examples=["Rosa Isela Rodriguez Olvera"],
    )
    direccion: str = Field(
        min_length=25,
        max_length=200,
        description="Ingrese la nueva dirección del cliente",
        examples=["Calle Hidalgo 123, Colonia Centro, Monterrey, Nuevo Leon"],
    )


class ClientesListaRespuesta(BaseModel):
    success: bool
    total: int
    clientes: list[ClienteRespuesta]


class SolicitudDesactivar(BaseModel):
    motivo: str | None = Field(
        default=None,
        max_length=200,
        description="Ingrese el motivo de la baja del cliente",
    )


class DesactivacionRespuesta(BaseModel):
    success: bool
    mensaje_confirmacion: str
    cliente: ClienteRespuesta
    motivo: str | None = None


class ConsumoRespuesta(BaseModel):
    id_consumo: int
    id_cliente: int
    consumo_luz: float
    fecha_registro: datetime


class ConsumoCrear(BaseModel):
    id_cliente: int = Field(ge=1, description="Identificador del cliente")
    consumo_luz: float = Field(
        ge=0,
        description="Ingrese el consumo en kWh",
        examples=[250.5],
    )
    fecha_registro: datetime | None = Field(
        default=None,
        description="Ingrese la fecha y hora de la lectura",
        examples=["2026-10-12 09:30:00"],
    )


class ConsumoParcial(BaseModel):
    consumo_luz: float | None = Field(
        default=None,
        ge=0,
        description="Ingrese el nuevo consumo en kWh",
    )
    fecha_registro: datetime | None = Field(
        default=None,
        description="Ingrese la nueva fecha y hora de la lectura",
    )


class ConsumoOperacionRespuesta(BaseModel):
    success: bool
    mensaje: str
    consumo: ConsumoRespuesta


class ConsumoReporte(BaseModel):
    id_consumo: int
    id_cliente: int
    nombre_cliente: str
    direccion: str
    consumo_luz: float
    fecha_registro: datetime
    tarifa: float
    total_pagar: float


class ConsumosReporteRespuesta(BaseModel):
    success: bool
    total: int
    tarifa_actual: float
    total_general_pagar: float
    consumos: list[ConsumoReporte]



class TarifaActualizar(BaseModel):
    tarifa: float = Field(
        ge=0,
        description="Nueva tarifa por kWh",
        examples=[1.35],
    )


class TarifaRespuesta(BaseModel):
    success: bool
    mensaje: str
    tarifa_actual: float
