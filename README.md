# Blog de Supersticiones y Mitos en Bolivia

Este proyecto es una API RESTful para un blog sobre supersticiones y mitos en Bolivia, desarrollada con FastAPI, SQLite, y SQLAlchemy.

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- Python (versión 3.7+)
- Docker
- Postman

Además, se recomienda tener conocimientos básicos de:

- Python (hasta Programación Orientada a Objetos)
- Conceptos básicos de bases de datos
- Uso básico de Git

## Guía de Configuración y Desarrollo

Sigue estos pasos para configurar y desarrollar el proyecto:

### 1. Configuración del Entorno

1. Clona este repositorio:
   ```
   git clone https://github.com/pyladieslp/FastAPI-Workshop
   cd FastAPI-Workshop
   ```

2. Crea un entorno virtual:
   ```
   python -m venv venv
   ```
   
   > Un entorno virtual en Python es un espacio aislado donde puedes instalar dependencias específicas para tu proyecto sin afectar a otros proyectos o al sistema global.

3. Activa el entorno virtual:
   - En Windows:
     ```
     venv\Scripts\activate
     ```
   - En macOS y Linux:
     ```
     source venv/bin/activate
     ```

4. Instala las dependencias:
   ```
   pip install fastapi uvicorn sqlalchemy pydantic
   ```

   > - FastAPI: Un moderno y rápido framework web para construir APIs con Python.
   > - Uvicorn: Un servidor ASGI de alto rendimiento compatible con FastAPI.
   > - SQLAlchemy: Una biblioteca de SQL y ORM (Object Relational Mapper) para Python.
   > - Pydantic: Una biblioteca para validación de datos y gestión de configuraciones usando anotaciones de tipo Python.

5. Crea un archivo `requirements.txt`:
   ```
   pip freeze > requirements.txt
   ```
   
   > Este archivo lista todas las dependencias del proyecto, facilitando su reproducción en otros entornos.

### 2. Estructura del Proyecto

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

> - `app/`: Contiene el código principal de la aplicación.
> - `tests/`: Directorio para pruebas unitarias y de integración.
> - `requirements.txt`: Lista de dependencias del proyecto.
> - `README.md`: Documentación principal del proyecto (este archivo).

### 3. Configuración de la Base de Datos

1. Crea el archivo `app/database.py` con el siguiente contenido:

```python
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Configuración de la base de datos SQLite
sqlite_file_name = "database.sqlite"  # Nombre del archivo de la base de datos
base_dir = os.path.dirname(os.path.realpath(__file__))  # Directorio base del proyecto
database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"  # URL de la base de datos

# Crear el motor de la base de datos
engine = create_engine(database_url, echo=True)

# Crear una fábrica de sesiones
Session = sessionmaker(bind=engine)

# Crear una base para los modelos declarativos
Base = declarative_base()
```

> Este script configura SQLAlchemy para usar una base de datos SQLite. 
> - `create_engine`: Crea una instancia del motor de base de datos.
> - `sessionmaker`: Crea una fábrica para generar sesiones de base de datos.
> - `declarative_base`: Crea una clase base para definir modelos declarativos de SQLAlchemy.

### 4. Modelado de Datos

1. Crea el archivo `app/models.py` con los siguientes modelos:

```python
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Text, ForeignKey
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
    nombre = Column(String, unique=True, index=True)
    
    # Establece una relación con la tabla Texto
    textos = relationship("Texto", back_populates="categoria")
```

> Estos modelos definen la estructura de las tablas en la base de datos.
> - `Texto`: Representa un texto (mito o superstición) en el blog.
> - `Categoria`: Representa una categoría para clasificar los textos.
> - `relationship`: Establece relaciones entre las tablas (uno a muchos en este caso).

### 5. Schemas de Pydantic

1. Crea el archivo `app/schemas.py` con los siguientes schemas:

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

class CategoriaBase(BaseModel):
    nombre: str

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int
    class Config:
        from_attributes = True  # Permite la conversión de modelos ORM a modelos Pydantic

class TextoCreate(TextoBase):
    pass

class Texto(TextoBase):
    id: int
    categoria: Categoria
    
    class Config:
        from_attributes = True  # Permite la conversión de modelos ORM a modelos Pydantic
```

> Los schemas de Pydantic definen la estructura de los datos para la entrada y salida de la API.
> - `BaseModel`: Clase base para todos los modelos Pydantic.
> - `from_attributes = True`: Permite la conversión automática entre modelos SQLAlchemy y Pydantic.

### 6. Configuración Inicial de la API

1. Crea el archivo `app/main.py` con la configuración básica de FastAPI:

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

> Este script configura la aplicación FastAPI y define un endpoint para crear nuevos textos.
> - `FastAPI()`: Crea una instancia de la aplicación FastAPI.
> - `Base.metadata.create_all(bind=engine)`: Crea las tablas en la base de datos.
> - `@app.post('/textos/')`: Define un endpoint POST para crear nuevos textos.

### 7. Ejecución de la Aplicación

Para ejecutar la aplicación, usa el siguiente comando:

```
uvicorn app.main:app --reload
```

> - `uvicorn`: El servidor ASGI que ejecutará nuestra aplicación.
> - `app.main:app`: Indica a Uvicorn dónde encontrar la instancia de la aplicación FastAPI.
> - `--reload`: Hace que el servidor se reinicie automáticamente cuando detecta cambios en el código.

La API estará disponible en `http://localhost:8000`. Puedes acceder a la documentación interactiva en `http://localhost:8000/docs`.

> FastAPI genera automáticamente una documentación interactiva (Swagger UI) que permite probar los endpoints de la API directamente desde el navegador.

## Próximos Pasos

- Implementar operaciones CRUD completas para Textos y Categorías.
- Añadir funcionalidades de búsqueda y filtrado.
- Implementar paginación para manejar grandes cantidades de datos.
- Mejorar la documentación de la API con descripciones detalladas de cada endpoint.
- Agregar pruebas unitarias y de integración para asegurar la calidad del código.
- Implementar autenticación y autorización para proteger ciertos endpoints.

