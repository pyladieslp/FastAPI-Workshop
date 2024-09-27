# Taller de Desarrollo Backend con FastAPI - Sesión 2

Este proyecto es una API RESTful para un blog sobre supersticiones y mitos en Bolivia, desarrollada con FastAPI, SQLite y SQLAlchemy.
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

- **Python** (versión 3.7+)
- **Docker desktop instalado**
- **Postman instalado o parecido**
## 1. Postman <a name="postman"></a>

**Postman** es una herramienta utilizada para probar APIs de manera sencilla y efectiva. En este taller, usaremos Postman para hacer solicitudes HTTP (GET, POST, PUT, DELETE) y verificar que los endpoints que hemos creado en FastAPI funcionan correctamente.

- **Python** (hasta Programación Orientada a Objetos)
- **Conceptos básicos de bases de datos**
- **Uso básico de Git**
- **¿Cómo se usa?**
    - Instala Postman y crea un nuevo request.
    - Introduce la URL de tu API (por ejemplo, `http://localhost:8000/textos`) y selecciona el método HTTP que desees probar (GET, POST, etc.).
    - Añade parámetros en el **Body** o **Params** si es necesario.
    - Envía la solicitud y verifica la respuesta en la sección **Response**.

---

## 2. Documentación Automática con Swagger <a name="swagger"></a>

FastAPI genera automáticamente una **documentación interactiva** utilizando **Swagger**. Esto te permite explorar y probar tu API desde el navegador sin necesidad de herramientas externas como Postman.

#### a. Clonar el Repositorio

1. Clona este repositorio:
   ```bash
   git clone https://github.com/pyladieslp/FastAPI-Workshop
   cd FastAPI-Workshop
   ```

#### b. Crear un Entorno Virtual

2. Crea un entorno virtual:
   ```bash
   python -m venv venv
   ```
   
   > **¿Qué es un entorno virtual?**
   >
   > Un **entorno virtual** en Python es un espacio aislado donde puedes instalar dependencias específicas para tu proyecto sin afectar a otros proyectos o al sistema global. Esto garantiza que cada proyecto tenga sus propias versiones de paquetes y evita conflictos entre dependencias.

   **Nota para Usuarios de Windows:**
   
   Al crear y activar entornos virtuales en Windows, es posible que encuentres un error relacionado con permisos al intentar ejecutar archivos bash. Para resolverlo, asegúrate de ejecutar la terminal como **Administrador** o ajusta las políticas de ejecución de scripts de PowerShell:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
   Esto permite la ejecución de scripts locales no firmados, lo cual es necesario para activar el entorno virtual correctamente.

#### c. Activar el Entorno Virtual

3. Activa el entorno virtual:
   - **En Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **En macOS y Linux:**
     ```bash
     source venv/bin/activate
     ```

#### d. Instalar las Dependencias

4. Instala las dependencias necesarias:
   ```bash
   pip install fastapi uvicorn sqlalchemy pydantic
   ```

   > **Descripción de las Dependencias:**
   >
   > - **FastAPI**: Un moderno y rápido framework web para construir APIs con Python.
   > - **Uvicorn**: Un servidor ASGI de alto rendimiento compatible con FastAPI.
   > - **SQLAlchemy**: Una biblioteca de SQL y ORM (Object Relational Mapper) para Python.
   > - **Pydantic**: Una biblioteca para validación de datos y gestión de configuraciones usando anotaciones de tipo Python.

#### e. Crear un Archivo `requirements.txt`

5. Genera un archivo `requirements.txt` que lista todas las dependencias del proyecto:
   ```bash
   pip freeze > requirements.txt
   ```
   
   > **¿Por qué es importante `requirements.txt`?**
   >
   > Este archivo facilita la reproducción del entorno de desarrollo en otros sistemas, asegurando que todas las dependencias y sus versiones estén claramente especificadas.

### 2. Introducción a FastAPI

**FastAPI** es un framework moderno, rápido y eficiente para construir APIs con Python. Aprovecha las características de Python 3.7+ como las anotaciones de tipo para ofrecer validación automática de datos, generación de documentación interactiva y rendimiento optimizado.

#### Comandos Importantes de FastAPI

- **Crear una Aplicación Básica:**
  ```python
  from fastapi import FastAPI

  app = FastAPI()

  @app.get("/")
  def read_root():
      return {"Hello": "World"}
  ```

- **Ejecutar la Aplicación con Uvicorn:**
  ```bash
  uvicorn app.main:app --reload
  ```
  - `app.main:app`: Indica a Uvicorn dónde encontrar la instancia de la aplicación FastAPI.
  - `--reload`: Hace que el servidor se reinicie automáticamente cuando detecta cambios en el código.

#### Un "Hola Mundo" en FastAPI

1. Crea un archivo `hello.py` con el siguiente contenido:
   ```python
   from fastapi import FastAPI

   app = FastAPI()

   @app.get("/")
   def read_root():
       return {"message": "¡Hola Mundo!"}
   ```

2. Ejecuta la aplicación:
   ```bash
   uvicorn hello:app --reload
   ```

3. Accede a `http://localhost:8000` en tu navegador para ver el mensaje de "Hola Mundo".

4. Visita `http://localhost:8000/docs` para acceder a la documentación interactiva generada automáticamente por FastAPI.

### 3. Estructura del Proyecto

El proyecto tiene la siguiente estructura:

```
proyecto_blog/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── database.py
│
├── tests/
│   └── __init__.py
│
├── requirements.txt
└── README.md
```

> **Descripción de la Estructura:**
> 
> - `app/`: Contiene el código principal de la aplicación.
>   - `main.py`: Archivo principal donde se configura y ejecuta la aplicación FastAPI.
>   - `models.py`: Define los modelos de datos utilizando SQLAlchemy.
>   - `schemas.py`: Define los esquemas de Pydantic para la validación y serialización de datos.
>   - `database.py`: Configuración de la base de datos y conexión.
> - `tests/`: Directorio para pruebas unitarias y de integración.
> - `requirements.txt`: Lista de dependencias del proyecto.
> - `README.md`: Documentación principal del proyecto (este archivo).

### 4. Configuración de la Base de Datos

#### a. Creación del Archivo `database.py`

1. Crea el archivo `app/database.py` con el siguiente contenido:

    ```python
    import os
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, declarative_base

    # Configuración de la base de datos SQLite
    sqlite_file_name = "database.sqlite"  # Nombre del archivo de la base de datos
    base_dir = os.path.dirname(os.path.realpath(__file__))  # Directorio base del proyecto
    database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"  # URL de la base de datos

    # Crear el motor de la base de datos
    engine = create_engine(database_url, echo=True)

    # Crear una fábrica de sesiones
    SessionLocal = sessionmaker(bind=engine)

    # Crear una base para los modelos declarativos
    Base = declarative_base()
    ```

    > **Descripción del Archivo `database.py`:**
    >
    > Este script configura SQLAlchemy para usar una base de datos SQLite.
    > - `create_engine`: Crea una instancia del motor de base de datos que maneja la conexión.
    > - `sessionmaker`: Crea una fábrica para generar sesiones de base de datos que manejarán las transacciones.
    > - `declarative_base`: Crea una clase base para definir modelos declarativos de SQLAlchemy, facilitando la definición de tablas.

### 5. Modelado de Datos

#### a. Diseño del Esquema ER

Antes de definir los modelos, es importante diseñar el esquema Entidad-Relación (ER) para entender cómo se relacionan las entidades dentro de la base de datos.

**Relaciones:**

- **Un texto pertenece a una categoría** (`categoria_id` en el modelo `Texto`).
- **Una categoría puede tener varios textos** (relación uno a muchos).

Este diseño asegura que cada texto esté clasificado bajo una categoría específica, y cada categoría puede agrupar múltiples textos relacionados.

#### b. Creación del Archivo `models.py`

2. Crea el archivo `app/models.py` con los siguientes modelos:

    ```python
    from sqlalchemy.orm import relationship
    from sqlalchemy import Column, Integer, String, ForeignKey
    from .database import Base

    class Texto(Base):
        __tablename__ = "textos"
        
        id = Column(Integer, primary_key=True, index=True)
        titulo = Column(String, index=True)
        autor = Column(String)
        descripcion = Column(String)
        contenido = Column(String)
        region = Column(String)
        categoria_id = Column(Integer, ForeignKey("categorias.id"))
        
        # Establece una relación con la tabla Categoria
        categoria = relationship("Categoria", back_populates="textos")

    class Categoria(Base):
        __tablename__ = "categorias"
        id = Column(Integer, primary_key=True, index=True)
        nombre = Column(String, unique=True, index=True, nullable=False)
        
        # Establece una relación con la tabla Texto
        textos = relationship("Texto", back_populates="categoria")
    ```

    > **Descripción de los Modelos:**
    >
    > - **Texto**:
    >   - Representa un texto (mito o superstición) en el blog.
    >   - Campos:
    >     - `id`: Identificador único.
    >     - `titulo`: Título del texto.
    >     - `autor`: Autor del texto.
    >     - `descripcion`: Breve descripción del texto.
    >     - `contenido`: Contenido completo del texto.
    >     - `region`: Región de Bolivia relacionada con el texto.
    >     - `categoria_id`: Clave foránea que referencia a la categoría.
    >   > - **Relación**: Cada `Texto` pertenece a una `Categoria`.

    > - **Categoria**:
    >   - Representa una categoría para clasificar los textos.
    >   - Campos:
    >     - `id`: Identificador único.
    >     - `nombre`: Nombre de la categoría.
    >   > - **Relación**: Una `Categoria` puede tener múltiples `Textos`.

### 6. Schemas de Pydantic

#### a. Creación del Archivo `schemas.py`

3. Crea el archivo `app/schemas.py` con los siguientes schemas:

    ```python
    from pydantic import BaseModel
    from typing import List, Optional

    class CategoriaBase(BaseModel):
        nombre: str

    class CategoriaCreate(CategoriaBase):
        pass

    class Categoria(CategoriaBase):
        id: int
        textos: List['Texto'] = []

        class Config:
            orm_mode = True  # Permite la conversión de modelos ORM a modelos Pydantic

    class TextoBase(BaseModel):
        titulo: str
        autor: str
        descripcion: str
        contenido: str
        region: str
        categoria_id: int

    class TextoCreate(TextoBase):
        pass

    class Texto(TextoBase):
        id: int
        categoria: Categoria

        class Config:
            orm_mode = True  # Permite la conversión de modelos ORM a modelos Pydantic
    ```

    > **Descripción de los Schemas:**
    >
    > - **BaseModel**: Clase base de Pydantic para todos los modelos de datos.
    > - **CategoriaBase y TextoBase**: Definen los campos comunes para las operaciones de creación y lectura.
    > - **CategoriaCreate y TextoCreate**: Schemas utilizados para crear nuevas instancias en la base de datos.
    > - **Categoria y Texto**: Schemas utilizados para retornar datos al cliente, incluyendo relaciones.
    > - **`orm_mode = True`**: Permite que Pydantic convierta automáticamente los modelos ORM de SQLAlchemy a los schemas de Pydantic, facilitando la serialización de datos.

### 7. Configuración Inicial de la API

#### a. Creación del Archivo `main.py`

4. Crea el archivo `app/main.py` con la configuración básica de FastAPI:

    ```python
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    from app.database import Session, engine, Base
    from app.models import Texto
    from app.schemas import TextoCreate

    app = FastAPI()

    # Crea las tablas en la base de datos
    Base.metadata.create_all(bind=engine)

    @app.post('/textos/', tags=['Textos'])
    def create_textos(texto: TextoCreate):
        db = Session()
        new_texto = Texto(**texto.model_dump())  # Crea una instancia de Texto con los datos del schema
        db.add(new_texto)  # Añade el nuevo texto a la sesión de la base de datos
        db.commit()  # Confirma los cambios en la base de datos
        return JSONResponse(content={"message": "Se ha registrado con éxito"})
    ```

    > **Descripción del Archivo `main.py`:**
    >
    > Este script configura la aplicación FastAPI y define un endpoint para crear nuevos textos.

    > FastAPI(): Crea una instancia de la aplicación FastAPI.
    Base.metadata.create_all(bind=engine): Crea las tablas en la base de datos.
    @app.post('/textos/'): Define un endpoint POST para crear nuevos textos.
    >
    > - **Instanciación de FastAPI:**
    >   ```python
    >   app = FastAPI(title="Blog de Supersticiones y Mitos en Bolivia")
    >   ```
    >   Crea una instancia de la aplicación FastAPI con un título descriptivo.
    >
    > - **Creación de Tablas:**
    >   ```python
    >   Base.metadata.create_all(bind=engine)
    >   ```
    >   Crea todas las tablas definidas en los modelos si no existen ya en la base de datos.
    >
    > - **Endpoints:**
    >   - **`@app.post('/textos/')`**: Crea un nuevo texto.
    
> - **HTTP Status Codes Comunes en Backend:**
>   - `201 Created`: Indica que un recurso se ha creado exitosamente.
>   - `200 OK`: Solicitud exitosa.
>   - `400 Bad Request`: Solicitud malformada o inválida.
>   - `404 Not Found`: Recurso no encontrado.
>   - `500 Internal Server Error`: Error inesperado en el servidor.

### 8. Ejecución de la Aplicación

Para ejecutar la aplicación, usa el siguiente comando:

```bash
uvicorn app.main:app --reload
```

> **Descripción del Comando:**
> 
> - `uvicorn`: El servidor ASGI que ejecutará nuestra aplicación.
> - `app.main:app`: Indica a Uvicorn dónde encontrar la instancia de la aplicación FastAPI.
> - `--reload`: Hace que el servidor se reinicie automáticamente cuando detecta cambios en el código.

#### Acceso a la API y Documentación

- **URL Principal de la API:**
  ```
  http://localhost:8000
  ```

- **Documentación Interactiva (Swagger UI):**
  ```
  http://localhost:8000/docs
  ```
  
  > **¿Qué es `http://localhost:8000/docs`?**
  >
  > FastAPI genera automáticamente una documentación interactiva utilizando **Swagger UI**. Esta interfaz permite probar los endpoints de la API directamente desde el navegador, facilitando la interacción y prueba de los diferentes endpoints sin necesidad de herramientas externas.
> Algunos ejemplos los cuales puedes ir usando con el endpoint POST de texto:
```json
[
  {
    "titulo": "El Chupacabra",
    "autor": "Folclore Popular",
    "descripcion": "Criatura mítica de América Latina, descrita como un animal bípedo que ataca y drena la sangre del ganado, especialmente cabras.",
    "contenido": "Se dice que el Chupacabra es una criatura de ojos grandes y brillantes, con garras afiladas y una boca llena de dientes. A pesar de numerosas avistamientos reportados, nunca se han encontrado pruebas científicas de su existencia.",
    "region": "América Latina",
    "categoria_id": 1 // 1 = Criaturas Míticas
  },
  {
    "titulo": "La Llorona",
    "autor": "Folclore Mexicano",
    "descripcion": "Leyenda mexicana sobre una mujer que ahogó a sus hijos y ahora vaga por la noche llorando y buscando a sus pequeños.",
    "contenido": "Se dice que su llanto desgarrador puede escucharse cerca de ríos y cuerpos de agua, y que aquellos que la ven están condenados a una mala suerte.",
    "region": "México",
    "categoria_id": 2 // 2 = Espíritus
  },
  {
    "titulo": "El Kraken",
    "autor": "Mitología Nórdica",
    "descripcion": "Monstruosa criatura marina de la mitología nórdica, descrita como un pulpo gigante capaz de hundir barcos.",
    "contenido": "El Kraken era temido por los marineros, quienes creían que podía surgir de las profundidades del océano y atacar sus embarcaciones con sus tentáculos.",
    "region": "Escandinavia",
    "categoria_id": 1
  },
  {
    "titulo": "La Sirenita",
    "autor": "Hans Christian Andersen",
    "descripcion": "Cuento de hadas danés sobre una sirena que desea convertirse en humana para poder estar con el príncipe que ama.",
    "contenido": "Esta historia trata sobre el sacrificio, la belleza y la naturaleza humana, y ha sido adaptada en numerosas ocasiones al cine y la televisión.",
    "region": "Dinamarca",
    "categoria_id": 3 // 3 = Cuentos de Hadas
  },
  {
    "titulo": "El Yeti",
    "autor": "Folclore del Himalaya",
    "descripcion": "Criatura similar a un simio que habita en las montañas del Himalaya, según las leyendas locales.",
    "contenido": "El Yeti, también conocido como el Abominable Hombre de las Nieves, ha sido objeto de numerosas expediciones y avistamientos, aunque nunca se han encontrado pruebas concluyentes de su existencia.",
    "region": "Himalaya",
    "categoria_id": 1
  }
]

```

- **Documentación Alternativa (ReDoc):**
  ```
  http://localhost:8000/redoc
  ```
  
  > **ReDoc** es otra interfaz de documentación generada automáticamente por FastAPI, ofreciendo una presentación diferente y algunas funcionalidades adicionales comparadas con Swagger UI.

## Próximos pasos
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

## Recursos Adicionales

- **[Documentación Oficial de FastAPI](https://fastapi.tiangolo.com/)**
- **[SQLAlchemy Documentation](https://www.sqlalchemy.org/)**
- **[Pydantic Documentation](https://pydantic-docs.helpmanual.io/)**
- **[Uvicorn Documentation](https://www.uvicorn.org/)**
- **[Docker Documentation](https://docs.docker.com/)**
- **[Postman Documentation](https://learning.postman.com/docs/getting-started/introduction/)**

