from pydantic import BaseModel
from typing import Optional

class TextoBase(BaseModel):
    titulo: str
    autor: str
    descripcion: str
    contenido: str
    region: str
    categoria_id:int
    # No incluimos imagen_url aquí porque se generará en el servidor

class CategoriaBase(BaseModel):
    nombre:str
    

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int
    class Config:
        # Convierte instancias de SQLAlchemy a modelos Pydantic que se utilizan en respuestas de API
        from_attributes = True  
class TextoCreate(TextoBase):
    pass

class Texto(TextoBase):
    id: int
    imagen_url: Optional[str]  # Añadimos este campo
    categoria: Optional[Categoria]
    
    class Config:
       # orm_mode =True
        from_attributes = True  
