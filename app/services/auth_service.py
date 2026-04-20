from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.core.security import verify_password, create_access_token

def autenticar_usuario(db: Session, email: str, password: str):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()

    if not usuario:
        return "USER_NOT_FOUND"

    if not verify_password(password, usuario.password):
        return "INVALID_PASSWORD"

    token = create_access_token({
        "sub": str(usuario.id),
        "email": usuario.email
    })

    return token