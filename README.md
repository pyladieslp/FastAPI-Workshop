# Sesion 3: Implementación de carga de imágenes en FastAPI

## Paso 1: Modificar el archivo `models.py`

Abre el archivo `models.py` y realiza los siguientes cambios:

```python
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from .database import Base

class Texto(Base):
    __tablename__ = "textos"
    
    id = Column(Integer, primary_key = True, index=True)
    titulo = Column(String, index=True)
    autor = Column(String)
    descripcion = Column(String)
    contenido = Column(String)
    region = Column(String)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    # Nuevo campo para almacenar la ruta de la imagen
    imagen_url = Column(String)
    
    # Relación muchos-a-uno: un texto pertenece a una categoría
    categoria = relationship("Categoria", back_populates="textos")

# La clase Categoria permanece sin cambios
```

### Explicación:

- Añadimos un nuevo campo `imagen_url = Column(String)` a la clase `Texto`.
- Este campo almacenará la URL o ruta de la imagen asociada al texto.
- Utilizamos `String` como tipo de dato porque almacenaremos la ruta como una cadena de texto.

## Paso 2: Modificar el archivo `schemas.py`

Abre el archivo `schemas.py` y realiza los siguientes cambios:

```python
from pydantic import BaseModel
from typing import Optional

class TextoBase(BaseModel):
    titulo: str
    autor: str
    descripcion: str
    contenido: str
    region: str
    categoria_id: int
    # No incluimos imagen_url aquí porque se generará en el servidor

class CategoriaBase(BaseModel):
    nombre: str

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int
    class Config:
        from_attributes = True

class TextoCreate(TextoBase):
    pass

class Texto(TextoBase):
    id: int
    imagen_url: Optional[str]  # Añadimos este campo
    categoria: Optional[Categoria]
    
    class Config:
        from_attributes = True
```

### Explicación:

- En la clase `Texto`, añadimos `imagen_url: Optional[str]`.
- Usamos `Optional` porque la imagen podría no estar presente en todos los casos.
- No incluimos `imagen_url` en `TextoBase` o `TextoCreate` porque la URL se generará en el servidor después de cargar la imagen.
- `from_attributes = True` permite a Pydantic leer los datos directamente de los modelos de SQLAlchemy.

## Paso 3: Modificar el archivo `main.py`

Abre el archivo `main.py` y realiza los siguientes cambios:

```python
import os
import uuid
from typing import Annotated, List, Optional
from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import or_
from app import schemas
from app import models
from app.database import Session, engine, Base
from app.models import Categoria, Texto
from app.schemas import CategoriaCreate, TextoCreate, Texto as TextoSchema
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import joinedload

app = FastAPI()

# Configurar la carpeta static para servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

#Modificando Swagger
app.title = "Mi aplicacion FastAPI"

Base.metadata.create_all(bind=engine)

# Función auxiliar para guardar la imagen
def save_image(file: UploadFile) -> str:
    # Generar un nombre único para el archivo
    file_name = f"{uuid.uuid4()}{os.path.splitext(file.filename)[1]}"
    file_path = os.path.join("static", "images", file_name)
    
    # Guardar el archivo
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    
    return f"/static/images/{file_name}"

@app.post('/textos/', tags=['Textos'])
async def create_textos(
    titulo: str = Form(...),
    autor: str = Form(...),
    descripcion: str = Form(...),
    contenido: str = Form(...),
    region: str = Form(...),
    categoria_id: int = Form(...),
    imagen: UploadFile = File(...)
):
    # Guardar la imagen y obtener la URL
    imagen_url = save_image(imagen)
    
    # Crear el objeto Texto
    texto_data = {
        "titulo": titulo,
        "autor": autor,
        "descripcion": descripcion,
        "contenido": contenido,
        "region": region,
        "categoria_id": categoria_id,
        "imagen_url": imagen_url
    }
    
    db = Session()
    new_texto = Texto(**texto_data)
    db.add(new_texto)
    db.commit()
    db.refresh(new_texto)
    
    return JSONResponse(content={"message": "Se ha registrado con éxito", "texto": jsonable_encoder(new_texto)})

# Modificar la función get_textos para incluir la URL de la imagen
@app.get('/textos', tags=['Textos'] )
def get_textos() -> List[TextoSchema]:
    db = Session()
    result = db.query(Texto).options(joinedload(Texto.categoria)).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

# Las demás funciones permanecen sin cambios
```

### Explicación detallada:

1. Importaciones adicionales:
   ```python
   import os
   import uuid
   from fastapi import File, UploadFile, Form
   from fastapi.staticfiles import StaticFiles
   ```
   - `os`: Para manejar rutas de archivos.
   - `uuid`: Para generar nombres únicos para las imágenes.
   - `File`, `UploadFile`: Para manejar la carga de archivos.
   - `Form`: Para recibir datos de formulario.
   - `StaticFiles`: Para servir archivos estáticos.

2. Configuración de archivos estáticos:
   ```python
   app.mount("/static", StaticFiles(directory="static"), name="static")
   ```
   - Esto permite a FastAPI servir archivos estáticos desde la carpeta "static".
   - Los archivos en esta carpeta serán accesibles públicamente.

3. Función auxiliar para guardar imágenes:
   ```python
   def save_image(file: UploadFile) -> str:
       file_name = f"{uuid.uuid4()}{os.path.splitext(file.filename)[1]}"
       file_path = os.path.join("static", "images", file_name)
       
       with open(file_path, "wb") as buffer:
           buffer.write(file.file.read())
       
       return f"/static/images/{file_name}"
   ```
   - `uuid.uuid4()`: Genera un identificador único para evitar conflictos de nombres.
   - `os.path.splitext(file.filename)[1]`: Obtiene la extensión del archivo original.
   - `os.path.join()`: Construye la ruta del archivo de manera segura y compatible con diferentes sistemas operativos.
   - `with open(...) as buffer`: Abre un archivo en modo escritura binaria y lo cierra automáticamente al finalizar.
   - `buffer.write(file.file.read())`: Lee el contenido del archivo subido y lo escribe en el nuevo archivo.

4. Modificación de la función `create_textos`:
   ```python
   @app.post('/textos/', tags=['Textos'])
   async def create_textos(
       titulo: str = Form(...),
       autor: str = Form(...),
       descripcion: str = Form(...),
       contenido: str = Form(...),
       region: str = Form(...),
       categoria_id: int = Form(...),
       imagen: UploadFile = File(...)
   ):
   ```
   - Usamos `Form(...)` para cada campo de texto, lo que permite recibir datos de un formulario HTML.
   - `UploadFile = File(...)`: Especifica que esperamos un archivo subido.
   - La función se declara como `async` para manejar la carga de archivos de manera asíncrona.

5. Guardado de la imagen y creación del texto:
   ```python
   imagen_url = save_image(imagen)
   
   texto_data = {
       "titulo": titulo,
       "autor": autor,
       "descripcion": descripcion,
       "contenido": contenido,
       "region": region,
       "categoria_id": categoria_id,
       "imagen_url": imagen_url
   }
   
   db = Session()
   new_texto = Texto(**texto_data)
   db.add(new_texto)
   db.commit()
   db.refresh(new_texto)
   ```
   - Guardamos la imagen y obtenemos la URL.
   - Creamos un diccionario con todos los datos del texto, incluyendo la URL de la imagen.
   - Creamos una nueva instancia de `Texto` con estos datos.
   - Añadimos el nuevo texto a la base de datos, hacemos commit y refrescamos para obtener el ID asignado.

6. Modificación de `get_textos`:
   ```python
   @app.get('/textos', tags=['Textos'] )
   def get_textos() -> List[TextoSchema]:
       db = Session()
       result = db.query(Texto).options(joinedload(Texto.categoria)).all()
       return JSONResponse(status_code=200, content=jsonable_encoder(result))
   ```
   - Usamos `joinedload(Texto.categoria)` para cargar la categoría relacionada en una sola consulta, optimizando el rendimiento.
   - `jsonable_encoder(result)` convierte los objetos SQLAlchemy en un formato JSON serializable.

## Paso 4: Configuración adicional

1. Crear la carpeta para imágenes:
   - Crea una carpeta llamada `images` dentro de la carpeta `static` en la raíz de tu proyecto.
   - Estructura: `/static/images/`

2. Actualizar los requisitos del proyecto:
   - Ejecuta: `pip install python-multipart`
   - Añade `python-multipart` a tu archivo `requirements.txt`.


## Paso 5: Probemos
Ejecuta:
```
uvicorn app.main:app --reloa
```
y haz la prueba mediantes 

`http://0.0.0.0:8000/docs`

---

# Dockerizar el Proyecto FastAPI con Carga de Imágenes

## 1. Crea el `Dockerfile`

Crea o actualiza el archivo `Dockerfile` en el directorio raíz del proyecto con el siguiente contenido:

```Dockerfile
# Usa una imagen oficial de Python como base
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de dependencias (requirements.txt) al contenedor
COPY requirements.txt .

# Instala las dependencias desde el archivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de la aplicación al contenedor
COPY ./app /app/app

# Crea el directorio para almacenar las imágenes
RUN mkdir -p /app/static/images

# Establece los permisos adecuados para el directorio de imágenes
RUN chmod 777 /app/static/images

# Expone el puerto 8000 para la aplicación FastAPI
EXPOSE 8000

# Comando para ejecutar la aplicación FastAPI con Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Explicación de los cambios:
- Añadimos `RUN mkdir -p /app/static/images` para crear el directorio donde se almacenarán las imágenes.
- `RUN chmod 777 /app/static/images` establece permisos amplios para asegurar que la aplicación pueda escribir en este directorio.

## 2. Actualizar el archivo `docker-compose.yml`

Actualiza el archivo `docker-compose.yml` en la raíz del proyecto con el siguiente contenido:

```yaml
version: '3.8'

services:
  fastapi-app:
    build: .
    container_name: fastapi-container
    ports:
      - "8000:8000"
    volumes:
      - .:/app
      - ./static/images:/app/static/images
    environment:
      - PYTHONUNBUFFERED=1
```

### Explicación de los cambios:
- Añadimos un nuevo volumen `- ./static/images:/app/static/images` que monta el directorio de imágenes del host en el contenedor. Esto asegura que las imágenes subidas persistan incluso si el contenedor se reinicia o se elimina.

## 3. Actualizar el archivo `.dockerignore`

Asegúrate de que tu archivo `.dockerignore` en la raíz del proyecto incluya lo siguiente:

```dockerignore
env/
__pycache__/
*.pyc
*.pyo
*.pyd
*.db
static/images/*
```

### Explicación:
- Añadimos `static/images/*` para evitar copiar las imágenes existentes al construir la imagen de Docker. Las imágenes se manejarán a través del volumen montado.

## 4. Asegurarse de tener el archivo `requirements.txt` actualizado

Verifica que tu archivo `requirements.txt` incluya todas las dependencias necesarias, incluyendo las nuevas para manejar la carga de archivos:

```
fastapi
uvicorn
pydantic
sqlalchemy
python-multipart
```

## 5. Construir y ejecutar la aplicación en Docker

Una vez que hayas actualizado todos los archivos, sigue estos pasos para construir y ejecutar la aplicación:

1. **Construir la imagen** de Docker:
   ```bash
   docker-compose build
   ```

2. **Iniciar el contenedor**:
   ```bash
   docker-compose up
   ```

   Esto levantará el contenedor de la aplicación FastAPI. La API estará disponible en `http://localhost:8000`.

## 6. Verificación de la aplicación

- Abre tu navegador y accede a la API FastAPI a través de `http://localhost:8000`.
- La documentación interactiva de Swagger estará disponible en `http://localhost:8000/docs`.
- Prueba la funcionalidad de carga de imágenes para asegurarte de que las imágenes se están guardando correctamente en el directorio `static/images`.
