
from typing import Annotated, List, Optional
from fastapi import FastAPI, HTTPException # type: ignore
from fastapi.responses import JSONResponse # type: ignore
from sqlalchemy import or_ # type: ignore
from app import schemas
from app import models
from app.database import Session, engine, Base
from app.models import Categoria, Texto
from app.schemas import CategoriaCreate, TextoCreate
from fastapi.encoders import jsonable_encoder # type: ignore
from sqlalchemy.orm import joinedload # type: ignore

app = FastAPI()

#Modificando Swagger
app.title = "Mi aplicacion FastAPI"

Base.metadata.create_all(bind=engine)

@app.post('/textos/', tags=['Textos'])
def create_textos(texto: TextoCreate):
    db = Session()
    new_texto = Texto(**texto.model_dump())
    db.add(new_texto)
    db.commit()
    return JSONResponse(content={"message": "Se ha registrado con exito"})

@app.get('/textos', tags=['Textos'] )
def get_textos() -> List[schemas.Texto]:
    db = Session()
    result = db.query(Texto).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.get('/textos/{texto_id}', tags=['Textos'])
def get_texto_by_id(texto_id: int) -> schemas.Texto:
    db = Session()
    texto = db.query(Texto).filter(Texto.id == texto_id).first()
    
    if texto is None:
        raise HTTPException(status_code=404, detail="Texto no encontrado")
    
    return JSONResponse(status_code=200, content=jsonable_encoder(texto))


# modificar
@app.put('/textos/{id}', tags=['Textos'])
def update_texto(id: int, texto: schemas.TextoCreate):
    db = Session()
    result =  db.query(Texto).filter(Texto.id == id).first()
    if not result:
        return HTTPException(status_code=404, detail="Texto no encontrado")
    result.titulo = texto.titulo
    result.autor = texto.autor
    result.descripcion = texto.descripcion
    result.contenido= texto.contenido
    result.region = texto.region
    result.categoria_id = texto.categoria_id
    db.commit()    
    return HTTPException(status_code=200, detail="Se ha modificado correctamente")
    
#Borrar
@app.delete('/textosborrar/{id}', tags=['Textos'] )
def delete_textos(id: int):
    db = Session()
    result =  db.query(Texto).filter(Texto.id == id).first()
    if not result:
        return HTTPException(status_code=404, detail="Texto no encontrado")
    db.delete(result)
    db.commit()
    return HTTPException(status_code=200, detail="Se ha eliminado correctamente")

#CRUD CATEGORIAS
@app.post('/categoria/', tags=['Categorias'])
def create_categoria(categoria: schemas.CategoriaCreate):
    db = Session()
    new_categoria = Categoria(**categoria.model_dump())
    db.add(new_categoria)
    db.commit()
    return JSONResponse(content={"message": "Se ha registrado con exito"})

@app.get('/categorias', tags=['Categorias'] )
def get_categoria() -> List[schemas.Categoria]:
    db = Session()
    result = db.query(Categoria).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.get('/categorias/{categoria_id}', tags=['Categorias'])
def get_categoria_by_id(categoria_id: int) -> schemas.Categoria:
    db = Session()
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    
    return JSONResponse(status_code=200, content=jsonable_encoder(categoria))

@app.put('/categorias/{id}', tags=['Categorias'])
def update_categoria(id: int, categoria: schemas.CategoriaCreate):
    db = Session()
    result =  db.query(Categoria).filter(Categoria.id == id).first()
    if not result:
        return HTTPException(status_code=404, detail="Categoria no encontrado")
    result.nombre = categoria.nombre
    db.commit()    
    return HTTPException(status_code=200, detail="Se ha modificado correctamente")
    
#Borrar

@app.delete('/categoria/{id}', tags=['Categorias'] )
def delete_categoria(id: int):
    db = Session()
    result =  db.query(Categoria).filter(Categoria.id == id).first()
    if not result:
        return HTTPException(status_code=404, detail="Categoria no encontrado")
    db.delete(result)
    db.commit()
    return HTTPException(status_code=200, detail="Se ha eliminado correctamente")


#FILTRAFDO POR CATEGORIA

@app.get('/textos/categoria/{categoria_id}', tags=['Textos'])
def get_texto_by_id(categoria_id: int) -> List[schemas.Texto]:
    db = Session()
    textos = db.query(Texto).filter(Texto.categoria_id == categoria_id).all()
    if textos is None:
        raise HTTPException(status_code=404, detail="Textos no encontrados en la categoria")
    return JSONResponse(status_code=200, content=jsonable_encoder(textos))

@app.get('/textos/buscar/', tags=['Textos'])
def buscar_textos(
    palabra: Optional[str] = None,
) -> List[schemas.Texto]:
    with Session() as db:
        query = db.query(Texto).options(joinedload(Texto.categoria))  # Carga la relación 'categoria'
        if palabra:
            palabra = palabra.strip()
            query = query.filter(
                or_(
                    Texto.titulo.ilike(f"%{palabra}%"),
                    Texto.descripcion.ilike(f"%{palabra}%"),
                    Texto.contenido.ilike(f"%{palabra}%")
                )
            )
        
        textos = query.all()
        if not textos:
            raise HTTPException(status_code=404, detail="No se encontraron textos que coincidan con los criterios de búsqueda")
        return textos


@app.get("/")
def read_root():
    return {"Hello": "World"}