import time
from datetime import date, datetime
from fastapi import FastAPI, HTTPException, Path, Query, Request

from modelo_base import (
    ClienteActualizar,
    ClienteCrear,
    ClienteRespuesta,
    ClientesListaRespuesta,
    ConsumoCrear,
    ConsumoOperacionRespuesta,
    ConsumoParcial,
    ConsumoReporte,
    ConsumoRespuesta,
    ConsumosReporteRespuesta,
    DesactivacionRespuesta,
    SolicitudDesactivar,
    TarifaActualizar,
    TarifaRespuesta,
)


app = FastAPI(
    title="API DE LA CFE - Clientes y consumo de energia",
    description=(
        "API REST para clientes, lecturas de consumo electrico (kWh) y la tarifa actual de CFE."
        "Equipo conformado por Rosa Isela, Angel Sebastian, y Teresa Margarita ."
        "Materia Desarrollo Web Grupo 033"
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

clientes: list[dict] = []
consumos: list[dict] = []
tarifa_actual = 1.20

siguiente_id_cliente = 1
siguiente_id_consumo = 1


@app.middleware("http")
async def medir_tiempo(request: Request, call_next):
    inicio = time.perf_counter()
    response = await call_next(request)
    tiempo = time.perf_counter() - inicio
    response.headers["X-Tiempo-Procesamiento"] = f"{tiempo:.4f}s"
    return response


def buscar_cliente(id_cliente: int) -> dict:
    """Devuelve el cliente o lanza 404 si no existe."""
    for cliente in clientes:
        if cliente["id_cliente"] == id_cliente:
            return cliente
    raise HTTPException(
        status_code=404,
        detail=f"El cliente con id {id_cliente} no existe",
    )


def buscar_consumo(id_consumo: int) -> dict:
    """Devuelve el consumo o lanza 404 si no existe."""
    for consumo in consumos:
        if consumo["id_consumo"] == id_consumo:
            return consumo
    raise HTTPException(
        status_code=404,
        detail=f"El consumo con id {id_consumo} no existe",
    )

def validar_fecha_no_futura(fecha: datetime | None) -> None:
    """Lanza 400 si la fecha de la lectura es posterior al momento actual."""
    if fecha is None:
        return
    ahora = datetime.now(fecha.tzinfo) if fecha.tzinfo else datetime.now()
    if fecha > ahora:
        raise HTTPException(
            status_code=400,
            detail="La fecha de la lectura no puede ser una fecha futura",
        )
    


@app.get(
    "/v1/api/clientes",
    summary="Para consultar todos los clientes",
    description="Devuelve todos los clientes registrados, activos e inactivos.",
    response_description="Indicador de éxito, total y lista de clientes",
    response_model=ClientesListaRespuesta,
    tags=["Clientes"],
    operation_id="consultarClientes",
)
def consultar_clientes() -> ClientesListaRespuesta:
    return ClientesListaRespuesta(
        success=True,
        total=len(clientes),
        clientes=[ClienteRespuesta(**c) for c in clientes],
    )


@app.post(
    "/v1/api/clientes",
    summary="Registrar un nuevo cliente",
    description="Al momento de crear un cliente. El id se genera solo y el cliente sale activo.",
    response_description="Cliente creado correctamente",
    response_model=ClienteRespuesta,
    status_code=201,
    tags=["Clientes"],
    operation_id="registrarCliente",
)

def registrar_cliente(datos: ClienteCrear) -> ClienteRespuesta:
    global siguiente_id_cliente

    cliente = {
        "id_cliente": siguiente_id_cliente,
        "nombre_cliente": datos.nombre_cliente,
        "direccion": datos.direccion,
        "active": True,
    }
    clientes.append(cliente)
    siguiente_id_cliente += 1
    return ClienteRespuesta(**cliente)


@app.put(
    "/v1/api/clientes/{id_cliente}",
    summary="Actualizar la informacion de un cliente",
    description="Ingresa la informacion a reemplazar: el nombre y la direccion del cliente indicado.",
    response_description="Cliente actualizado correctamente",
    response_model=ClienteRespuesta,
    tags=["Clientes"],
    operation_id="actualizarCliente",
)
def actualizar_cliente(
    id_cliente: int = Path(..., ge=1, description="Identificador del cliente"),
    datos: ClienteActualizar = ...,
) -> ClienteRespuesta:
    cliente = buscar_cliente(id_cliente) 
    cliente["nombre_cliente"] = datos.nombre_cliente
    cliente["direccion"] = datos.direccion
    return ClienteRespuesta(**cliente)


@app.delete(
    "/v1/api/clientes/{id_cliente}",
    summary="Desactivar un cliente",
    description=(
        "El cliente no se elimina de la lista, solo se cambia active = false. "
    ),
    response_description="Confirmacion de desactivacion",
    response_model=DesactivacionRespuesta,
    tags=["Clientes"],
    operation_id="desactivarCliente",
)
def desactivar_cliente(
    id_cliente: int = Path(..., ge=1, description="Identificador del cliente"),
    datos: SolicitudDesactivar | None = None,
) -> DesactivacionRespuesta:
    cliente = buscar_cliente(id_cliente) 

    if not cliente["active"]:
        raise HTTPException(
            status_code=400,
            detail=f"El cliente con id {id_cliente} ya esta inactivo",
        )

    cliente["active"] = False
    return DesactivacionRespuesta(
        success=True,
        mensaje_confirmacion="Cliente desactivado correctamente",
        cliente=ClienteRespuesta(**cliente),
        motivo=datos.motivo if datos else None,
    )



@app.post(
    "/v1/api/consumos",
    summary="Registrar una nueva lectura de consumo",
    description=(
        "Registra el consumo en kWh de un cliente ACTIVO. "
        "Si no se envia fecha_registro se usa la fecha y hora actuales."
    ),
    response_description="Lectura registrada correctamente",
    response_model=ConsumoOperacionRespuesta,
    status_code=201,
    tags=["Consumos"],
    operation_id="registrarConsumo",
)

def registrar_consumo(datos: ConsumoCrear) -> ConsumoOperacionRespuesta:
    global siguiente_id_consumo

    cliente = buscar_cliente(datos.id_cliente) 
    if not cliente["active"]:
        raise HTTPException(
            status_code=400,
            detail=(
                f"El cliente con id {datos.id_cliente} esta inactivo, "
                "no se pueden registrar consumos"
            ),
        )
    validar_fecha_no_futura(datos.fecha_registro)
    consumo = {
        "id_consumo": siguiente_id_consumo,
        "id_cliente": datos.id_cliente,
        "consumo_luz": datos.consumo_luz,
        "fecha_registro": datos.fecha_registro or datetime.now(),
    }
    consumos.append(consumo)
    siguiente_id_consumo += 1

    return ConsumoOperacionRespuesta(
        success=True,
        mensaje="Lectura registrada correctamente",
        consumo=ConsumoRespuesta(**consumo),
    )

@app.get(
    "/v1/api/clientes/{id_cliente}/consumos",
    summary="Consultar las lecturas de un cliente",
    description=(
        "Muestra solo las lecturas (consumo y fecha) del cliente indicado. "
        "Devuelve error si el cliente no existe, esta inactivo."
    ),
    response_description="Lecturas del cliente",
    response_model=list[ConsumoRespuesta],
    tags=["Consumos"],
    operation_id="consultarLecturasPorCliente",
)
def consultar_lecturas_cliente(
    id_cliente: int = Path(..., ge=1, description="Identificador del cliente"),
) -> list[ConsumoRespuesta]:
    cliente = buscar_cliente(id_cliente)

    if not cliente["active"]:
        raise HTTPException(
            status_code=400,
            detail=f"El cliente con id {id_cliente} esta inactivo",
        )

    lecturas = [c for c in consumos if c["id_cliente"] == id_cliente]

    lecturas.sort(key=lambda c: c["fecha_registro"])
    return [ConsumoRespuesta(**c) for c in lecturas]


@app.get(
    "/v1/api/consumos",
    summary="Consulta y reporte de consumos",
    description=(
        "Muestra solo los consumos de clientes ACTIVOS, con el consumo, la fecha, "
        "la tarifa actual y el total a pagar. Se puede filtrar por rango de fechas."
    ),
    response_description="Reporte de consumos con totales",
    response_model=ConsumosReporteRespuesta,
    tags=["Consumos"],
    operation_id="consultarConsumos",
)
def consultar_consumos(
    fecha_inicio: date | None = Query(
        default=None,
        description="Incluye lecturas desde esta fecha (AAAA-MM-DD)",
        examples=["2026-10-01"],
    ),
    fecha_fin: date | None = Query(
        default=None,
        description="Incluye lecturas hasta esta fecha (AAAA-MM-DD)",
        examples=["2026-10-31"],
    ),
) -> ConsumosReporteRespuesta:
    if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
        raise HTTPException(
            status_code=400,
            detail="fecha_inicio no puede ser mayor que fecha_fin",
        )

    filas: list[ConsumoReporte] = []
    for consumo in consumos:
        cliente = buscar_cliente(consumo["id_cliente"])

        if not cliente["active"]:
            continue

        dia = consumo["fecha_registro"].date()
        if fecha_inicio and dia < fecha_inicio:
            continue
        if fecha_fin and dia > fecha_fin:
            continue

        filas.append(
            ConsumoReporte(
                id_consumo=consumo["id_consumo"],
                id_cliente=cliente["id_cliente"],
                nombre_cliente=cliente["nombre_cliente"],
                direccion=cliente["direccion"],
                consumo_luz=consumo["consumo_luz"],
                fecha_registro=consumo["fecha_registro"],
                tarifa=tarifa_actual,
                total_pagar=round(consumo["consumo_luz"] * tarifa_actual, 2),
            )
        )

    filas.sort(key=lambda fila: fila.fecha_registro)

    return ConsumosReporteRespuesta(
        success=True,
        total=len(filas),
        tarifa_actual=tarifa_actual,
        total_general_pagar=round(sum(f.total_pagar for f in filas), 2),
        consumos=filas,
    )


@app.patch(
    "/v1/api/consumos/{id_consumo}",
    summary="Actualizar una lectura de consumo",
    description=(
        "Modifica el consumo y/o la fecha de una lectura existente. "
        "No se puede actualizar si el cliente esta inactivo."
    ),
    response_description="Lectura actualizada correctamente",
    response_model=ConsumoOperacionRespuesta,
    tags=["Consumos"],
    operation_id="actualizarConsumo",
)
def actualizar_consumo(
    id_consumo: int = Path(..., ge=1, description="Identificador de la lectura"),
    datos: ConsumoParcial = ...,
) -> ConsumoOperacionRespuesta:
    consumo = buscar_consumo(id_consumo) 
    cliente = buscar_cliente(consumo["id_cliente"])

    if not cliente["active"]:
        raise HTTPException(
            status_code=400,
            detail=(
                f"El cliente con id {cliente['id_cliente']} esta inactivo, "
                "no se puede actualizar el consumo"
            ),
        )

    if datos.consumo_luz is None and datos.fecha_registro is None:
        raise HTTPException(
            status_code=400,
            detail="Debes enviar al menos consumo_luz o fecha_registro",
        )
    
    validar_fecha_no_futura(datos.fecha_registro)

    if datos.consumo_luz is not None:
        consumo["consumo_luz"] = datos.consumo_luz
    if datos.fecha_registro is not None:
        consumo["fecha_registro"] = datos.fecha_registro

    return ConsumoOperacionRespuesta(
        success=True,
        mensaje="Lectura actualizada correctamente",
        consumo=ConsumoRespuesta(**consumo),
    )


@app.get(
    "/v1/api/tarifa",
    summary="Consultar la tarifa actual",
    description="Devuelve la tarifa por kWh que se usa en los calculos.",
    response_description="Tarifa vigente",
    response_model=TarifaRespuesta,
    tags=["Tarifa"],
    operation_id="consultarTarifa",
)
def consultar_tarifa() -> TarifaRespuesta:
    return TarifaRespuesta(
        success=True,
        mensaje="Tarifa actual consultada correctamente",
        tarifa_actual=tarifa_actual,
    )


@app.put(
    "/v1/api/tarifa",
    summary="Modificar la tarifa actual",
    description="Cambia la tarifa por kWh. Se usa en los calculos posteriores.",
    response_description="Tarifa actualizada correctamente",
    response_model=TarifaRespuesta,
    tags=["Tarifa"],
    operation_id="actualizarTarifa",
)

def actualizar_tarifa(datos: TarifaActualizar) -> TarifaRespuesta:
    global tarifa_actual

    tarifa_actual = datos.tarifa
    return TarifaRespuesta(
        success=True,
        mensaje="Tarifa actualizada correctamente",
        tarifa_actual=tarifa_actual,
    )
