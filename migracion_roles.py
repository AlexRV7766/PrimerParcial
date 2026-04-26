import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine
from sqlalchemy import text

def run_migration():
    with engine.connect() as conn:
        print("Iniciando migración manual...")
        
        # Migración tabla taller
        try:
            conn.execute(text("ALTER TABLE taller ADD COLUMN usuario_id INTEGER REFERENCES usuario(id) ON DELETE SET NULL;"))
            print("Columna 'usuario_id' añadida a la tabla 'taller'.")
        except Exception as e:
            print(f"La columna 'usuario_id' en 'taller' quizás ya existe o hubo un error: {e}")
            
        # Migración tabla tecnico
        try:
            conn.execute(text("ALTER TABLE tecnico ADD COLUMN usuario_id INTEGER REFERENCES usuario(id) ON DELETE SET NULL;"))
            print("Columna 'usuario_id' añadida a la tabla 'tecnico'.")
        except Exception as e:
            print(f"La columna 'usuario_id' en 'tecnico' quizás ya existe o hubo un error: {e}")
            
        conn.commit()
        print("Migración finalizada.")

if __name__ == "__main__":
    run_migration()
