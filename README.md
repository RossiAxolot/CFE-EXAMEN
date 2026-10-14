# CFE-EXAMEN
API REST con SWAGGER con PYTHON Y FASTAPI con la libreria de PYDANTIC para validaciones. Metodos GET. PUT. POST. PATCH. DELETE. CON HTTP DE RESPUESTA: 200- 201- 400 - 404 - 422 

Previamente se necesita tener instalado PYTHON desde la pagina oficial o microsoft store con la casilla "Add Python to PATH"
y con la version mas actual la cual se puede consultar desde el simbolo del sistema CMD con el comando:
python --version

Para el entorno virtual se creo con el siguiente comando:
python -m venv .venv

Para activar el entorno virtual
.\.venv\Scripts\Activate.ps1

Para instalar las dependencias desde el archivo requirements.txt
pip install -r requirements.txt

Para instalar las dependencias necesarias en el entorno:
pip install fastapi uvicorn pydantic

Para iniciar la aplicacion se ejecuta en la terminal del proyecto:
uvicorn main:app --reload

Donde:
main es el nombre del archivo de Python. Puede llamarse de cualquier otra forma pero asi lo definimos nosotros
app es el nombre de la variable que definimos dentro de nuestro codigo donde se creo la instancia de FastApi

app = FastAPI(
    title="API CFE - Clientes y consumo de energia",
    description=(
        "API REST para administrar clientes, lecturas de consumo electrico (kWh) "
        "y la tarifa actual de CFE. Los datos viven en memoria (listas de Python)."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

--reload es el que activa el reinicio automatico cada vez que se guarda un cambio en el codigo entonces el servidor se reiniciara solo sin que tengamos que prender y apagar de forma manual

Para visualizar por medio de Swagger se genera la documentacion interactiva gracias a Pydantic y FastApi se genera de forma automatica y para ver la API es por medio de http://127.0.0.1:8000/docs.
