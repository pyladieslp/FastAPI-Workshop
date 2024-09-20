# Taller de Desarrollo Backend con FastAPI - Sesión 2

Bienvenidos a la segunda sesión del taller sobre el desarrollo backend con **FastAPI**. En esta sesión, exploraremos conceptos clave como **Postman**, la **documentación automática con Swagger**, los **métodos HTTP**, y aprenderemos a implementar un CRUD para el modelo de **Categorías** y **Textos** en nuestra API RESTful. También cubriremos la interacción entre el **Frontend** y el **Backend** usando FastAPI, y cómo filtrar datos utilizando endpoints específicos.

## Tabla de Contenidos
1. [Postman: Herramienta de prueba](#postman)
2. [Documentación automática con Swagger](#swagger)
3. [Métodos HTTP en FastAPI](#metodos-http)
4. [¿Qué es una API RESTful?](#api-restful)
5. [Interacción entre Frontend y Backend](#interaccion-frontend-backend)
6. [EndPoints para CRUD de Textos](#crud-textos)
7. [EndPoints para CRUD de Categorías](#crud-categorias)
8. [Filtrado de Textos](#filtrado-textos)

---

## 1. Postman <a name="postman"></a>

**Postman** es una herramienta utilizada para probar APIs de manera sencilla y efectiva. En este taller, usaremos Postman para hacer solicitudes HTTP (GET, POST, PUT, DELETE) y verificar que los endpoints que hemos creado en FastAPI funcionan correctamente.

- **¿Cómo se usa?**
    - Instala Postman y crea un nuevo request.
    - Introduce la URL de tu API (por ejemplo, `http://localhost:8000/textos`) y selecciona el método HTTP que desees probar (GET, POST, etc.).
    - Añade parámetros en el **Body** o **Params** si es necesario.
    - Envía la solicitud y verifica la respuesta en la sección **Response**.

---

## 2. Documentación Automática con Swagger <a name="swagger"></a>

FastAPI genera automáticamente una **documentación interactiva** utilizando **Swagger**. Esto te permite explorar y probar tu API desde el navegador sin necesidad de herramientas externas como Postman.

- **Acceso a Swagger**: Simplemente navega a `http://localhost:8000/docs` cuando tengas tu API en ejecución. Verás una interfaz que muestra todos los endpoints disponibles en tu aplicación y te permitirá hacer pruebas.

- **Modificando el título de Swagger**: En el archivo `main.py`, podemos personalizar el título de nuestra aplicación Swagger modificando esta línea:
    ```python
    app.title = "Mi aplicacion FastAPI"
    ```

---

## 3. Métodos HTTP en FastAPI <a name="metodos-http"></a>

En esta sesión, trabajaremos con los métodos HTTP principales:

- **GET**: Para obtener datos del servidor. Se usa en el endpoint `@app.get`.
- **POST**: Para enviar datos al servidor y crear nuevos registros. Se usa en el endpoint `@app.post`.
- **PUT**: Para actualizar un registro existente. Se usa en el endpoint `@app.put`.
- **DELETE**: Para eliminar un registro. Se usa en el endpoint `@app.delete`.

### Ejemplo de uso de métodos HTTP en FastAPI:
```python
@app.get('/textos', tags=['Textos'])
def get_textos() -> List[schemas.Texto]:
    # Inicia una sesión con la base de datos
    db = Session()
    # Recupera todos los textos almacenados
    result = db.query(Texto).all()
    # Retorna los resultados en formato JSON
    return JSONResponse(status_code=200, content=jsonable_encoder(result))
```

#### Explicación de los componentes:
- **`@app.get('/textos')`**: Decorador que define una ruta con el método GET, utilizada para obtener datos.
- **`db = Session()`**: Inicia una sesión de base de datos.
- **`db.query(Texto).all()`**: Recupera todos los registros del modelo `Texto`.
- **`jsonable_encoder(result)`**: Convierte los datos en un formato JSON adecuado para ser devueltos en la respuesta.
- **`return JSONResponse(status_code=200, content=...)`**: Devuelve los datos con un código HTTP 200 (OK).

---

## 4. ¿Qué es una API RESTful? <a name="api-restful"></a>

Una **API RESTful** sigue los principios de la arquitectura REST, lo que significa que utiliza métodos HTTP estándar y responde con recursos en formato JSON. En una API RESTful:

- **GET** recupera datos.
- **POST** envía datos.
- **PUT** modifica datos.
- **DELETE** elimina datos.

FastAPI nos facilita la creación de APIs RESTful de manera eficiente. Cada endpoint que creamos está diseñado para manejar una operación específica sobre los recursos (en este caso, Textos y Categorías).

---

## 5. Interacción entre Frontend y Backend <a name="interaccion-frontend-backend"></a>

El **Frontend** envía solicitudes HTTP al **Backend** a través de la API RESTful. El **Backend** procesa estas solicitudes, interactúa con la base de datos si es necesario, y devuelve una respuesta en formato JSON al Frontend.

- **Frontend**: Puede ser una aplicación web, móvil o incluso otra API.
- **Backend**: FastAPI maneja la lógica de negocio y la interacción con la base de datos.

Un ejemplo típico de interacción sería cuando el Frontend hace una solicitud `GET` para obtener la lista de textos:
```bash
GET /textos HTTP/1.1
```
FastAPI responde con una lista de textos en formato JSON.

---

## 6. CRUD para Textos <a name="crud-textos"></a>

El CRUD (Crear, Leer, Actualizar, Eliminar) es fundamental para cualquier aplicación. En este caso, implementamos CRUD para el modelo `Texto`.

### Crear Texto (POST):
```python
@app.post('/textos/', tags=['Textos'])
def create_textos(texto: TextoCreate):
    # Crea una sesión con la base de datos
    db = Session()
    # Crea una nueva instancia del modelo Texto a partir de los datos recibidos
    new_texto = Texto(**texto.model_dump())
    # Añade el nuevo texto a la base de datos
    db.add(new_texto)
    db.commit()
    # Devuelve una respuesta indicando que se ha creado correctamente
    return JSONResponse(content={"message": "Se ha registrado con exito"})
```

#### Explicación de los componentes:
- **`@app.post('/textos/')`**: Define un endpoint que responde a solicitudes POST para crear nuevos textos.
- **`texto: TextoCreate`**: El parámetro `texto` es del tipo `TextoCreate`, un esquema que define los campos requeridos para crear un texto.
- **`new_texto = Texto(**texto.model_dump())`**: Convierte el esquema `TextoCreate` en una instancia del modelo `Texto`.
- **`db.add(new_texto)`**: Añade el nuevo texto a la sesión de la base de datos.
- **`db.commit()`**: Confirma la transacción para guardar el nuevo texto en la base de datos.

---

### Leer todos los Textos (GET):
```python
@app.get('/textos', tags=['Textos'])
def get_textos() -> List[schemas.Texto]:
    # Inicia una sesión con la base de datos
    db = Session()
    # Recupera todos los textos almacenados
    result = db.query(Texto).all()
    # Retorna los resultados en formato JSON
    return JSONResponse(status_code=200, content=jsonable_encoder(result))
```

#### Explicación de los componentes:
- **`@app.get('/textos')`**: Endpoint GET para obtener todos los textos.
- **`List[schemas.Texto]`**: Indica que la función devuelve una lista de objetos `Texto` en formato de esquema.
- **`db.query(Texto).all()`**: Recupera todos los textos en la base de datos.

---

### Leer Texto por ID (GET):
```python
@app.get('/textos/{texto_id}', tags=['Textos'])
def get_texto_by_id(texto_id: int) -> schemas.Texto:
    # Inicia una sesión con la base de datos
    db = Session()
    # Busca un texto por su ID
    texto = db.query(Texto).filter(Texto.id == texto_id).first()
    # Verifica si el texto fue encontrado
    if texto is None:
        # Lanza una excepción si el texto no existe
        raise HTTPException(status_code=404, detail="Texto no encontrado")
    # Retorna el texto encontrado en formato JSON
    return JSONResponse(status_code=200, content=jsonable_encoder(texto))
```

#### Explicación de los componentes:
- **`texto_id: int`**: El parámetro `texto_id` es un entero que indica el ID del texto a buscar.
- **`db.query(Texto).filter(Texto.id == texto_id).first()`**: Busca el primer texto que coincida con el ID proporcionado.
- **`HTTPException(status_code=404)`**: Devuelve un error 404 si no se encuentra el texto.

---

### Actualizar Texto (PUT):
```python
@app.put('/textos/{id}', tags=['Textos

'])
def update_texto(id: int, updated_texto: TextoCreate):
    db = Session()
    texto = db.query(Texto).filter(Texto.id == id).first()
    if texto is None:
        raise HTTPException(status_code=404, detail="Texto no encontrado")
    texto.titulo = updated_texto.titulo
    texto.contenido = updated_texto.contenido
    db.commit()
    return JSONResponse(content={"message": "Se ha actualizado con exito"})
```

#### Explicación:
- **`@app.put('/textos/{id}')`**: Endpoint PUT para actualizar un texto específico.
- **`id: int`**: El ID del texto a actualizar.
- **`updated_texto: TextoCreate`**: Datos nuevos para actualizar el texto.

---

### Eliminar Texto (DELETE):
```python
@app.delete('/textos/{id}', tags=['Textos'])
def delete_texto(id: int):
    db = Session()
    texto = db.query(Texto).filter(Texto.id == id).first()
    if texto is None:
        raise HTTPException(status_code=404, detail="Texto no encontrado")
    db.delete(texto)
    db.commit()
    return JSONResponse(content={"message": "Texto eliminado con exito"})
```

#### Explicación:
- **`delete_texto(id: int)`**: Elimina el texto con el ID proporcionado.
- **`db.delete(texto)`**: Elimina el texto de la base de datos.
- **`db.commit()`**: Confirma la eliminación.

---

## 7. CRUD para Categorías <a name="crud-categorias"></a>

Se aplica un enfoque similar para el modelo de **Categorías**. Las funciones CRUD siguen la misma lógica que los ejemplos anteriores para **Textos**.

---

## 8. Filtrado de Textos <a name="filtrado-textos"></a>

El filtrado nos permite buscar textos que cumplan con ciertos criterios, como la **categoría**. Aquí implementamos un endpoint que devuelve textos filtrados por su categoría:

```python
@app.get('/textos/categoria/{categoria_id}', tags=['Textos'])
def get_textos_by_categoria(categoria_id: int):
    db = Session()
    textos = db.query(Texto).filter(Texto.categoria_id == categoria_id).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(textos))
```

#### Explicación:
- **`categoria_id: int`**: El ID de la categoría por la que queremos filtrar los textos.
- **`db.query(Texto).filter(Texto.categoria_id == categoria_id).all()`**: Recupera todos los textos que pertenecen a la categoría especificada.

---

## Dockerización del Proyecto

A continuación se describen los pasos para **dockerizar** este proyecto de FastAPI, lo que permitirá ejecutar la aplicación en un contenedor de Docker, facilitando su despliegue y portabilidad.

#### Requisitos Previos
- Tener instalado **Docker** y **Docker Compose** en tu máquina. Puedes descargar e instalar Docker desde [aquí](https://www.docker.com/get-started).

---

### 1. Crear un `Dockerfile`
Este archivo se encarga de definir la imagen de Docker con la configuración y las dependencias necesarias para ejecutar la aplicación FastAPI.

Crea un archivo llamado `Dockerfile` en el directorio raíz del proyecto con el siguiente contenido:

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

# Expone el puerto 8000 para la aplicación FastAPI
EXPOSE 8000

# Comando para ejecutar la aplicación FastAPI con Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Crear un archivo `docker-compose.yml`
El archivo `docker-compose.yml` te permitirá ejecutar la aplicación y sus servicios asociados (como una base de datos) en contenedores. Para este proyecto, solo ejecutaremos la aplicación FastAPI.

Crea un archivo `docker-compose.yml` en la raíz del proyecto con el siguiente contenido:

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
    environment:
      - PYTHONUNBUFFERED=1
```

#### Explicación:
- **build**: Construye la imagen de Docker utilizando el `Dockerfile`.
- **container_name**: Nombre del contenedor que se creará.
- **ports**: Mapea el puerto `8000` del contenedor al puerto `8000` de la máquina host, permitiendo acceder a la aplicación desde `http://localhost:8000`.
- **volumes**: Monta el directorio de trabajo local (`.`) dentro del contenedor, lo que permite realizar cambios en el código sin tener que reconstruir la imagen.
- **environment**: Asegura que los logs de la aplicación se muestren correctamente en tiempo real.

### 3. Crear un archivo `.dockerignore`
Para evitar que ciertos archivos innecesarios sean copiados al contenedor, como los archivos del entorno virtual, crea un archivo `.dockerignore` en la raíz del proyecto:

```dockerignore
env/
__pycache__/
*.pyc
*.pyo
*.pyd
*.db
```

### 4. Asegurarse de tener el archivo `requirements.txt`
El archivo `requirements.txt` debe contener todas las dependencias necesarias para que la aplicación funcione correctamente. Si aún no lo tienes, puedes generarlo con:

```bash
pip freeze > requirements.txt
```

Asegúrate de que incluya las siguientes dependencias (y otras necesarias):

```
fastapi
uvicorn
pydantic
sqlite3
```

### 5. Construir y ejecutar la aplicación en Docker

Una vez que tengas todos los archivos (`Dockerfile`, `docker-compose.yml`, `.dockerignore`, y `requirements.txt`), puedes construir y ejecutar la aplicación en un contenedor Docker siguiendo estos pasos:

1. **Construir la imagen** de Docker:
   ```bash
   docker-compose build
   ```

2. **Iniciar el contenedor**:
   ```bash
   docker-compose up
   ```

   Esto levantará el contenedor de la aplicación FastAPI. La API estará disponible en `http://localhost:8000`.

### 6. Verificación de la aplicación

Puedes abrir tu navegador y acceder a la API FastAPI a través de `http://localhost:8000`. Además, la documentación interactiva de Swagger estará disponible en `http://localhost:8000/docs`.

### Consideraciones futuras
- Si decides cambiar a una base de datos como **PostgreSQL** o **MySQL**, puedes añadir un servicio de base de datos en el archivo `docker-compose.yml` para gestionarla junto a tu aplicación FastAPI.
  
  Ejemplo de un servicio de PostgreSQL:
  ```yaml
  db:
    image: postgres:13
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
      POSTGRES_DB: mydb
  ```

Con esto, tu proyecto estará dockerizado, lo que facilita su despliegue y ejecución en cualquier entorno que soporte Docker.

---

### Reto: Carga imagenes en el CRUD

Para almacenar imágenes localmente en tu proyecto y asociarlas a cada entrada de la tabla `Texto`, puedes seguir estos pasos:

1. **Agregar un campo para la URL de la imagen** en el modelo `Texto`.
2. **Subir y almacenar las imágenes en un directorio dentro del proyecto**.
3. **Guardar la ruta local de la imagen en la base de datos** en lugar de una URL externa.

### Pasos para implementar la funcionalidad:

#### 1. Agregar el campo `url_imagen` al modelo `Texto`

Añadir un nuevo campo para almacenar la ruta local de la imagen en el modelo `Texto`:

```python
class Texto(Base):
    __tablename__ = "textos"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    autor = Column(String)
    descripcion = Column(String)
    contenido = Column(String)
    region = Column(String)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    
    # Relación muchos-a-uno: un texto pertenece a una categoría
    categoria = relationship("Categoria", back_populates="textos")
    
    # Nuevo campo para almacenar la URL de la imagen local
    url_imagen = Column(String)  # Ruta de la imagen dentro del sistema de archivos
```

#### 2. Subir las imágenes desde el frontend o Postman

Debes crear un endpoint para subir imágenes. FastAPI facilita la gestión de archivos con el uso de `File` y `UploadFile`. Así puedes manejar la subida de archivos:

```python
from fastapi import File, UploadFile
import shutil
import os

# Directorio donde se almacenarán las imágenes
IMAGES_DIR = "static/images"

# Crear el directorio si no existe
os.makedirs(IMAGES_DIR, exist_ok=True)

@app.post("/uploadfile/")
async def upload_image(file: UploadFile = File(...)):
    # Definir la ruta donde se guardará la imagen
    file_location = f"{IMAGES_DIR}/{file.filename}"
    
    # Guardar la imagen localmente
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    # Retornar la ruta de la imagen que luego se almacenará en la base de datos
    return {"file_url": file_location}
```

#### 3. Asignar la imagen al texto

Cuando subas un archivo, recibirás la ruta local en el formato `{"file_url": "static/images/imagen.jpg"}`. Luego, al crear un nuevo texto o actualizar uno existente, puedes almacenar la ruta de la imagen en la columna `url_imagen` del modelo `Texto`.

```python
@app.post("/textos/")
def create_texto(texto: TextoCreate, file_url: str):
    db = Session()
    nuevo_texto = Texto(
        titulo=texto.titulo,
        autor=texto.autor,
        descripcion=texto.descripcion,
        contenido=texto.contenido,
        region=texto.region,
        categoria_id=texto.categoria_id,
        url_imagen=file_url  # Guardamos la ruta de la imagen
    )
    db.add(nuevo_texto)
    db.commit()
    db.refresh(nuevo_texto)
    return nuevo_texto
```

#### 4. Servir las imágenes estáticas

Para que las imágenes se puedan acceder a través del navegador o en una API, FastAPI te permite servir archivos estáticos fácilmente. Solo tienes que configurar el servidor para que sirva el directorio de las imágenes:

```python
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")
```

Ahora, cualquier imagen almacenada en el directorio `static/images/` podrá ser accesible vía URL. Por ejemplo, una imagen guardada como `static/images/imagen.jpg` podrá visualizarse desde la URL `http://localhost:8000/static/images/imagen.jpg`.

### Resumen:
1. **Campo en el modelo**: Agregas `url_imagen` al modelo `Texto`.
2. **Subir imagen**: Creas un endpoint para subir archivos.
3. **Asignar imagen al texto**: Al crear o actualizar textos, puedes almacenar la ruta de la imagen.
4. **Servir archivos estáticos**: Configuras FastAPI para servir imágenes desde el directorio estático.

