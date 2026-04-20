from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.database import SessionLocal
from app.models.usuario import Usuario
from app.core.security import SECRET_KEY, ALGORITHM

security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    usuario = db.query(Usuario).filter(Usuario.id == int(user_id)).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    return usuario