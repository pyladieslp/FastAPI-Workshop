from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.database import Session, engine, Base
from app.models import Texto
from app.schemas import TextoCreate

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "¡Hola Mundo!"}

Base.metadata.create_all(bind=engine)

@app.post('/textos/', tags=['Textos'])
def create_textos(texto: TextoCreate):
    db = Session()
    new_texto = Texto(**texto.model_dump())
    db.add(new_texto)
    db.commit()
    return JSONResponse(content={"message": "Se ha registrado con exito"})
