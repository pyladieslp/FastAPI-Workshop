from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from .database import Base

class Texto(Base):
    __tablename__ = "textos"
    
    id = Column(Integer, primary_key = True, index=True)
    titulo = Column(String, index=True)
    autor = Column(String)
    descripcion = Column(String)
    contenido =Column(String)
    region = Column(String)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    
    # Relación muchos-a-uno: un texto pertenece a una categoría
    categoria = relationship("Categoria", back_populates="textos")
    
    
class Categoria(Base):
    __tablename__="categorias"
    id=Column(Integer, primary_key=True, index=True)
    nombre= Column(String, unique=True, index=True)
    
    # Relación uno-a-muchos: una categoría puede tener múltiples textos
    textos = relationship("Texto", back_populates="categoria")
    