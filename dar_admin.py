import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine
from sqlalchemy import text

def dar_admin():
    with engine.connect() as conn:
        print("Otorgando rol de administrador al primer usuario...")
        
        # Obtener el primer usuario
        result = conn.execute(text("SELECT id, email, nombre FROM usuario ORDER BY id ASC LIMIT 1;")).fetchone()
        
        if result:
            usuario_id = result[0]
            email = result[1]
            nombre = result[2]
            
            # Actualizar el rol
            conn.execute(text(f"UPDATE usuario SET rol = 'administrador' WHERE id = {usuario_id};"))
            conn.commit()
            print(f"¡Éxito! El usuario '{nombre}' ({email}) ahora es ADMINISTRADOR.")
        else:
            print("No hay ningún usuario en la base de datos. Registrá uno primero en el frontend y luego corré este script.")

if __name__ == "__main__":
    dar_admin()
