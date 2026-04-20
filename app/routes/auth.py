from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import autenticar_usuario
from app.core.deps import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
def login(datos: LoginRequest, db: Session = Depends(get_db)):
    resultado = autenticar_usuario(db, datos.email, datos.password)

    if resultado == "USER_NOT_FOUND":
        raise HTTPException(status_code=404, detail="Usuario no registrado")

    if resultado == "INVALID_PASSWORD":
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    return {"access_token": resultado}