from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate
from app.core.security import hash_password

def crear_usuario(db: Session, usuario: UsuarioCreate):
    nuevo = Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        password=hash_password(usuario.password),
        telefono=usuario.telefono
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def obtener_usuarios(db: Session):
    return db.query(Usuario).all()

def obtener_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def eliminar_usuario(db: Session, usuario_id: int):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario:
        db.delete(usuario)
        db.commit()
    return usuario