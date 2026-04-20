from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import (
    usuario,
    vehiculo,
    emergencia,
    evidencia,
    auth,
    taller,
    tecnico,
    historial,
    dispositivo,
    notificacion,
    pago
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(usuario.router)
app.include_router(vehiculo.router)
app.include_router(emergencia.router)
app.include_router(evidencia.router)
app.include_router(taller.router)
app.include_router(tecnico.router)
app.include_router(historial.router)
app.include_router(dispositivo.router)
app.include_router(notificacion.router)
app.include_router(pago.router)