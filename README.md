# API CFE - Clientes y consumo de energía

API REST con Swagger, desarrollada con Python y FastAPI, usando Pydantic para las validaciones.
Materia Desarrollo Web, grupo 033.

**Métodos HTTP:** GET, POST, PUT, PATCH, DELETE
**Códigos de respuesta:** 200, 201, 400, 404, 422

## Requisitos previos

Tener instalado Python 3.10 o superior, desde la página oficial o la Microsoft Store, marcando la casilla "Add Python to PATH". La versión se consulta en CMD con:

```bash
python --version
```

## Instalación y ejecución

1. Crear el entorno virtual:

```bash
python -m venv .venv
```

2. Activarlo (PowerShell en Windows):

```bash
.venv\Scripts\Activate.ps1
```

3. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

4. Iniciar la aplicación desde la carpeta del proyecto:

```bash
uvicorn main:app --reload
```

- `main` es el nombre del archivo de Python (`main.py`).
- `app` es la variable donde se creó la instancia de FastAPI dentro del código.
- `--reload` reinicia el servidor automáticamente cada vez que se guarda un cambio, sin tener que apagarlo y prenderlo a mano.

## Documentación (Swagger)

Gracias a FastAPI y Pydantic, la documentación interactiva se genera automáticamente:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/v1/api/clientes` | Consultar todos los clientes |
| POST | `/v1/api/clientes` | Registrar un cliente |
| PUT | `/v1/api/clientes/{id_cliente}` | Actualizar un cliente |
| DELETE | `/v1/api/clientes/{id_cliente}` | Desactivar un cliente (active = false) |
| POST | `/v1/api/consumos` | Registrar una lectura de consumo |
| GET | `/v1/api/clientes/{id_cliente}/consumos` | Lecturas de un cliente |
| GET | `/v1/api/consumos` | Reporte de consumos (filtro `fecha_inicio` y `fecha_fin`) |
| PATCH | `/v1/api/consumos/{id_consumo}` | Actualizar una lectura |
| GET | `/v1/api/tarifa` | Consultar la tarifa actual |
| PUT | `/v1/api/tarifa` | Modificar la tarifa actual |

## Nota

Los datos se guardan en memoria (listas de Python), por lo que se pierden al reiniciar el servidor.
