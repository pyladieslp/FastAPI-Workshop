# Blog de Supersticiones y Mitos en Bolivia

Este proyecto es una API RESTful para un blog sobre supersticiones y mitos en Bolivia, desarrollada con FastAPI, SQLite y SQLAlchemy.

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Python** (versión 3.7+)
- **Docker desktop instalado**
- **Postman instalado o parecido**

Además, se recomienda tener conocimientos básicos de:

- **Python** (hasta Programación Orientada a Objetos)
- **Conceptos básicos de bases de datos**
- **Uso básico de Git**

## Guía de Configuración y Desarrollo

Sigue estos pasos para configurar y desarrollar el proyecto:

### 1. Configuración del Entorno

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

- Implementar operaciones CRUD completas para Textos y Categorías.
- Añadir funcionalidades de búsqueda y filtrado.
- Implementar paginación para manejar grandes cantidades de datos.
- Mejorar la documentación de la API con descripciones detalladas de cada endpoint.
- Agregar pruebas unitarias y de integración para asegurar la calidad del código.
- Implementar autenticación y autorización para proteger ciertos endpoints.

## Recursos Adicionales

- **[Documentación Oficial de FastAPI](https://fastapi.tiangolo.com/)**
- **[SQLAlchemy Documentation](https://www.sqlalchemy.org/)**
- **[Pydantic Documentation](https://pydantic-docs.helpmanual.io/)**
- **[Uvicorn Documentation](https://www.uvicorn.org/)**
- **[Docker Documentation](https://docs.docker.com/)**
- **[Postman Documentation](https://learning.postman.com/docs/getting-started/introduction/)**

