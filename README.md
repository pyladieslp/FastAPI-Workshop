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

