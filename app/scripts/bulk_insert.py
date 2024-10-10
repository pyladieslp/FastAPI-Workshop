import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..models import Base, Categoria, Texto
from ..database import database_url

# Configuración de la base de datos
engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Obtener la ruta del directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

def cargar_json(nombre_archivo):
    file_path = os.path.join(current_dir, nombre_archivo)
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def bulk_insert():
    db = SessionLocal()
    try:
        # Cargar datos desde archivos JSON
        categorias = cargar_json('categorias.json')
        relatos = cargar_json('relatos.json')

        # Insertar categorías
        for categoria_data in categorias:
            categoria = Categoria(**categoria_data)
            db.add(categoria)
        db.commit()

        # Insertar relatos
        for relato_data in relatos:
            categoria_nombre = relato_data.pop('categoria_nombre')
            categoria = db.query(Categoria).filter_by(nombre=categoria_nombre).first()
            if categoria:
                relato_data['categoria_id'] = categoria.id
                texto = Texto(**relato_data)
                db.add(texto)
            else:
                print(f"Categoría no encontrada: {categoria_nombre}")
        db.commit()

        print("Inserción masiva completada con éxito.")
    except Exception as e:
        db.rollback()
        print(f"Error durante la inserción masiva: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    bulk_insert()