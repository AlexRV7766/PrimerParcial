from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Inicializa la configuración de Cloudinary
import app.core.cloudinary_config

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
    pago,
    asignacion
)

app = FastAPI(title="Emergencias Viales API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Error interno: {str(exc)}"},
    )

app.include_router(auth.router)
app.include_router(usuario.router)
app.include_router(vehiculo.router)
app.include_router(emergencia.router)
app.include_router(evidencia.router)
app.include_router(taller.router)
app.include_router(tecnico.router)
app.include_router(asignacion.router)
app.include_router(historial.router)
app.include_router(dispositivo.router)
app.include_router(notificacion.router)
app.include_router(pago.router)
